# This file is part of Archivematica.
#
# Copyright 2010-2013 Artefactual Systems Inc. <http://artefactual.com>
#
# Archivematica is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Archivematica is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Archivematica.  If not, see <http://www.gnu.org/licenses/>.

import collections
import ConfigParser
import logging
import os
import shutil
import subprocess
import sys

from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.forms.models import modelformset_factory
from django.shortcuts import redirect, render

from main import forms
from main import models
import components.administration.views_processing as processing_views
from components.administration.forms import AtomSettingsForm
from components.administration.forms import AgentForm
from components.administration.forms import ArchivistsToolkitConfigForm
from components.administration.forms import SettingsForm
from components.administration.forms import StorageSettingsForm
from components.administration.models import ArchivistsToolkitConfig
from components.administration.forms import TaxonomyTermForm
from django.http import Http404, HttpResponseNotAllowed, HttpResponseRedirect
from django.template import RequestContext
import components.decorators as decorators
from django.template import RequestContext
import components.helpers as helpers
import storageService as storage_service

sys.path.append('/usr/lib/archivematica/archivematicaCommon')
from version import get_full_version


logger = logging.getLogger('archivematica.dashboard')

""" @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      Administration
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ """

def administration(request):
    return redirect('components.administration.views.processing')

def failure_report(request, report_id=None):
    if report_id != None:
        report = models.Report.objects.get(pk=report_id)
        return render(request, 'administration/reports/failure_detail.html', locals())
    else:
        current_page_number = request.GET.get('page', '1')
        items_per_page = 10

        reports = models.Report.objects.all().order_by('-created')
        page = helpers.pager(reports, items_per_page, current_page_number)
        return render(request, 'administration/reports/failures.html', locals())

def delete_context(request, report_id):
    report = models.Report.objects.get(pk=report_id)
    prompt = 'Delete failure report for ' + report.unitname + '?'
    cancel_url = reverse("components.administration.views.failure_report")
    return RequestContext(request, {'action': 'Delete', 'prompt': prompt, 'cancel_url': cancel_url})

@decorators.confirm_required('simple_confirm.html', delete_context)
def failure_report_delete(request, report_id):
    models.Report.objects.get(pk=report_id).delete()
    messages.info(request, 'Deleted.')
    return redirect('components.administration.views.failure_report')

def failure_report_detail(request):
    return render(request, 'administration/reports/failure_report_detail.html', locals())

def atom_dips(request):
    upload_setting = models.StandardTaskConfig.objects.get(execute="upload-qubit_v0.0")
    form = AtomSettingsForm(request.POST or None, instance=upload_setting)
    if form.is_valid():
        form.save()
        messages.info(request, 'Saved.')

    hide_features = helpers.hidden_features()
    return render(request, 'administration/dips_atom_edit.html', locals())


def administration_atk_dips(request):
    atk = ArchivistsToolkitConfig.objects.all()[0]
    if request.POST:
        form = ArchivistsToolkitConfigForm(request.POST, instance=atk)
        usingpass =  atk.dbpass
        if form.is_valid():
            newatk = form.save()
            if newatk.dbpass != '' and newatk.dbpass != usingpass:
                usingpass = newatk.dbpass
            else:
                newatk.dbpass = usingpass
             #save this new form data into MicroServiceChoiceReplacementDic
            new_settings_string = '{{"%host%":"{}", "%port%":"{}", "%dbname%":"{}", "%dbuser%":"{}", "%dbpass%":"{}", \
                                   "%atuser%":"{}", "%restrictions%":"{}", "%object_type%":"{}", "%ead_actuate%":"{}", \
                                   "%ead_show%":"{}", "%use_statement%":"{}", "%uri_prefix%":"{}", "%access_conditions%":"{}", \
                                   "%use_conditions%":"{}"}}'.format(newatk.host, newatk.port, newatk.dbname, newatk.dbuser,
                                                                    usingpass,newatk.atuser,newatk.premis, newatk.object_type,
                                                                    newatk.ead_actuate, newatk.ead_show,newatk.use_statement,
                                                                    newatk.uri_prefix, newatk.access_conditions, newatk.use_conditions)
            logger.debug('new settings '+ new_settings_string)                       
            new_mscrDic = models.MicroServiceChoiceReplacementDic.objects.get(description='Archivists Toolkit Config')
            logger.debug('trying to save mscr ' + new_mscrDic.description)
            newatk.save()
            logger.debug('old: ' + new_mscrDic.replacementdic)
            new_mscrDic.replacementdic = new_settings_string
            logger.debug('new: ' + new_mscrDic.replacementdic)
            new_mscrDic.save() 
            logger.debug('done')
            messages.info(request, 'Saved.')
            valid_submission = True
    else:
        form = ArchivistsToolkitConfigForm(instance=atk)
    return render(request, 'administration/dips_atk_edit.html', locals())


def dips_formset():
    return modelformset_factory(
        models.MicroServiceChoiceReplacementDic,
        form=forms.MicroServiceChoiceReplacementDicForm,
        extra=0,
        can_delete=True
    )

def dips_handle_updates(request, link_id, ReplaceDirChoiceFormSet):
    valid_submission = True
    formset = None

    add_form = forms.MicroServiceChoiceReplacementDicForm()

    if request.method == 'POST':
        # if any new configuration data has been submitted, attempt to add it
        if request.POST.get('description', '') != '' or request.POST.get('replacementdic', '') != '':
            postData = request.POST.copy()
            postData['choiceavailableatlink'] = link_id

            add_form = forms.MicroServiceChoiceReplacementDicForm(postData)

            if add_form.is_valid():
                choice = models.MicroServiceChoiceReplacementDic()
                choice.choiceavailableatlink = link_id
                choice.description           = request.POST.get('description', '')
                choice.replacementdic        = request.POST.get('replacementdic', '')
                choice.save()

                # create new blank field
                add_form = forms.MicroServiceChoiceReplacementDicForm()

        formset = ReplaceDirChoiceFormSet(request.POST)

        # take note of formset validity because if submission was successful
        # we reload it to reflect
        # deletions, etc.
        valid_submission = formset.is_valid()

        if valid_submission:
            # save/delete partial data (without association with specific link)
            instances = formset.save()

            # restore link association
            for instance in instances:
                instance.choiceavailableatlink = link_id
                instance.save()
    return valid_submission, formset, add_form

def storage(request):
    try:
        locations = storage_service.get_location(purpose="AS")
    except:
        messages.warning(request, 'Error retrieving locations: is the storage server running? Please contact an administrator.')

    system_directory_description = 'Available storage'
    return render(request, 'administration/locations.html', locals())

def usage(request):
    usage_dirs = _usage_dirs()

    context = {'usage_dirs': usage_dirs}
    return render(request, 'administration/usage.html', context)

def _usage_dirs(calculate_usage=True):
    # Put spaces before directories contained by the spaces
    #
    # Description is optional, but either a path or a location purpose (used to
    # look up the path) should be specified
    #
    # If only certain sudirectories within a path should be deleted, set
    # 'subdirectories' to a list of them
    dir_defs = (
        ('shared', {
            'path': helpers.get_client_config_value('sharedDirectoryMounted')
        }),
        ('dips', {
            'description': 'DIP uploads',
            'path': os.path.join('watchedDirectories', 'uploadedDIPs'),
            'contained_by': 'shared'
        }),
        ('rejected', {
            'description': 'Rejected',
            'path': 'rejected',
            'contained_by': 'shared'
        }),
        ('failed', {
            'description': 'Failed',
            'path': 'failed',
            'contained_by': 'shared'
        }),
        ('tmp', {
            'description': 'Temporary file storage',
            'path': 'tmp',
            'contained_by': 'shared'
        })
    )

    dirs = collections.OrderedDict(dir_defs)

    # Resolve location paths and make relative paths absolute
    for _, dir_spec in dirs.iteritems():
        if 'contained_by' in dir_spec:
            # If contained, make path absolute
            space = dir_spec['contained_by']
            absolute_path = os.path.join(dirs[space]['path'], dir_spec['path'])
            dir_spec['path'] = absolute_path

            if calculate_usage:
                dir_spec['size'] = dirs[space]['size']
                dir_spec['used'] = _usage_get_directory_used_bytes(dir_spec['path'])
        elif calculate_usage:
            # Get size/usage of space
            space_path = dir_spec['path']
            dir_spec['size'] = _usage_check_directory_volume_size(space_path)
            dir_spec['used'] = _usage_get_directory_used_bytes(space_path)

    return dirs

def _usage_check_directory_volume_size(path):
    # Get volume size (in 512 byte blocks)
    try:
        output = subprocess.check_output(["df", path])

        # Second line returns disk usage-related values
        usage_summary = output.split("\n")[1]

        # Split value by whitespace and size (in blocks)
        size = usage_summary.split()[1]

        return int(size) * 512
    except Exception, e:
        logger.exception(str(e))
        return 0

def _usage_get_directory_used_bytes(path):
    """ Get total usage in bytes """
    try:
        output = subprocess.check_output(["du", "--bytes", "--summarize", path])
        return output.split("\t")[0]
    except Exception, e:
        logger.exception(str(e))
        return 0

def clear_context(request, dir_id):
    usage_dirs = _usage_dirs(False)
    prompt = 'Clear ' + usage_dirs[dir_id]['description'] + '?'
    cancel_url = reverse("components.administration.views.usage")
    return RequestContext(request, {'action': 'Delete', 'prompt': prompt, 'cancel_url': cancel_url})

@user_passes_test(lambda u: u.is_superuser, login_url='/forbidden/')
@decorators.confirm_required('simple_confirm.html', clear_context)
def usage_clear(request, dir_id):
    if request.method == 'POST':
        usage_dirs = _usage_dirs(False)
        dir_info = usage_dirs[dir_id]

        # Prevent shared directory from being cleared
        if dir_id == 'shared' or not dir_info:
            raise Http404

        # Determine if specific subdirectories need to be cleared, rather than
        # whole directory
        if 'subdirectories' in dir_info:
            dirs_to_empty = [os.path.join(dir_info['path'], subdir) for subdir in dir_info['subdirectories']] 
        else:
            dirs_to_empty = [dir_info['path']]

        # Attempt to clear directories
        successes = []
        errors = []

        for directory in dirs_to_empty:
            try:
                for entry in os.listdir(directory):
                    entry_path = os.path.join(directory, entry)
                    if os.path.isfile(entry_path):
                        os.unlink(entry_path)
                    else:
                        shutil.rmtree(entry_path)
                successes.append(directory)
            except Exception, e:
                logger.exception(str(e))
                errors.append(str(e))

        # If any deletion attempts successed, summarize in flash message
        if len(successes):
            message = 'Cleared %s.' % ', '.join(successes)
            messages.info(request, message)

        # Show flash message for each error encountered
        for error in errors:
            messages.error(request, error)

        return redirect('components.administration.views.usage')
    else:
        return HttpResponseNotAllowed()

def sources(request):
    try:
        locations = storage_service.get_location(purpose="TS")
    except:
        messages.warning(request, 'Error retrieving locations: is the storage server running? Please contact an administrator.')

    system_directory_description = 'Available transfer source'
    return render(request, 'administration/locations.html', locals())

def processing(request):
    return processing_views.index(request)

def premis_agent(request):
    agent = models.Agent.objects.get(pk=2)
    if request.POST:
        form = AgentForm(request.POST, instance=agent)
        if form.is_valid():
            messages.info(request, 'Saved.')
            form.save()
    else:
        form = AgentForm(instance=agent)

    hide_features = helpers.hidden_features()
    return render(request, 'administration/premis_agent.html', locals())

def api(request):
    if request.method == 'POST':
        whitelist = request.POST.get('whitelist', '')
        helpers.set_setting('api_whitelist', whitelist)
        messages.info(request, 'Saved.')
    else:
        whitelist = helpers.get_setting('api_whitelist', '127.0.0.1')

    hide_features = helpers.hidden_features()
    return render(request, 'administration/api.html', locals())

def taxonomy(request):
    taxonomies = models.Taxonomy.objects.all().order_by('name')
    page = helpers.pager(taxonomies, 20, request.GET.get('page', 1))
    return render(request, 'administration/taxonomy.html', locals())

def terms(request, taxonomy_uuid):
    taxonomy = models.Taxonomy.objects.get(pk=taxonomy_uuid)
    terms = taxonomy.taxonomyterm_set.order_by('term')
    page = helpers.pager(terms, 20, request.GET.get('page', 1))
    return render(request, 'administration/terms.html', locals())

def term_detail(request, term_uuid):
    term = models.TaxonomyTerm.objects.get(pk=term_uuid)
    taxonomy = term.taxonomy
    if request.POST:
        form = TaxonomyTermForm(request.POST, instance=term)
        if form.is_valid():
            form.save()
            messages = [{
              'text': 'Saved.'
            }]
    else:
        form = TaxonomyTermForm(instance=term)

    return render(request, 'administration/term_detail.html', locals())

def term_delete_context(request, term_uuid):
    term = models.TaxonomyTerm.objects.get(pk=term_uuid)
    prompt = 'Delete term ' + term.term + '?'
    cancel_url = reverse("components.administration.views.term_detail", args=[term_uuid])
    return RequestContext(request, {'action': 'Delete', 'prompt': prompt, 'cancel_url': cancel_url})

@decorators.confirm_required('simple_confirm.html', term_delete_context)
def term_delete(request, term_uuid):
    if request.method == 'POST':
        term = models.TaxonomyTerm.objects.get(pk=term_uuid)
        term.delete()
        return HttpResponseRedirect(reverse('components.administration.views.terms', args=[term.taxonomy_id]))

def general(request):
    toggleableSettings = {
        'dashboard_administration_atom_dip_enabled':
            'Hide AtoM DIP upload link',
        'dashboard_administration_dspace_enabled':
            'Hide DSpace transfer type',
    }
    initial_data = dict(models.DashboardSetting.objects.all().values_list(
        'name', 'value'))
    interface_form = SettingsForm(request.POST or None, prefix='interface',
        reverse_checkboxes=toggleableSettings)
    storage_form = StorageSettingsForm(request.POST or None, prefix='storage',
        initial=initial_data)

    if interface_form.is_valid() and storage_form.is_valid():
        interface_form.save()
        storage_form.save()
        messages.info(request, 'Saved.')

    dashboard_uuid = helpers.get_setting('dashboard_uuid')
    try:
        pipeline = storage_service._get_pipeline(dashboard_uuid)
    except Exception :
        messages.warning(request, "Storage server inaccessible.  Please contact an administrator or update storage service URL below.")
    else:
        if not pipeline:
            messages.warning(request, "This pipeline is not registered with the storage service or has been disabled in the storage service.  Please contact an administrator.")
    hide_features = helpers.hidden_features()
    return render(request, 'administration/general.html', locals())

def version(request):
    version = get_full_version()
    agent_code = models.Agent.objects.get(identifiertype="preservation system").identifiervalue
    return render(request, 'administration/version.html', locals())
