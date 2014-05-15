from os.path import basename
from django.utils.html import conditional_escape, format_html
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.forms.widgets import CheckboxInput
from form_utils.widgets import ImageWidget
from django.forms.widgets import ClearableFileInput


class BetterFileInput(ClearableFileInput):
    # Javascript available through assets:
    # widget_js_better_file_input or widget_js_all
    template_with_initial = u"""
        <div class="field-clear">
            <span class="field-clear-initial">%(initial)s</span>
            <script>document.write('<span class="field-clear-check-button pure-button pure-button-xsmall pure-button-error">Remove</span><span class="field-clear-cancel pure-button-xsmall pure-button pure-button-hidden">Cancel</span>')</script>
            <div class="browse-box">%(input)s</div>
            <noscript>%(clear_template)s</noscript>
            <script>document.write('<div class="field-clear-hidden-input pure-button-hidden">%(clear)s</div>')</script>
        </div>"""
    template_with_clear = u"""
        <label for="%(clear_checkbox_id)s" class="field-clear-check">
            Remove file: %(clear)s (tick and save)
        </label>"""

    def render(self, name, value, attrs=None):
        '''Same render method as ClearableFileInput has except that it wraps
        displayed file name with os.path.basename for nicer output.'''
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = '%(input)s'
        substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)

        if value and hasattr(value, "url"):
            template = self.template_with_initial
            substitutions['initial'] = format_html(u'<a href="{0}">{1}</a>',
                                                   value.url,
                                                   basename(force_text(value)))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)

    def value_from_datadict(self, data, files, name):
        '''
        Practically same as ClearableFileInput except that when user
        contradicts themselves, we return upload (upload wins).
        '''
        upload = super(ClearableFileInput, self).value_from_datadict(data, files, name)
        if not self.is_required and CheckboxInput().value_from_datadict(
                data, files, self.clear_checkbox_name(name)) and not upload:
            # False signals to clear any existing value, as opposed to just None
            return False
        return upload


class BetterImageInput(ClearableFileInput, ImageWidget):
    template = u"""
            <span class="field-clear-initial">%(image)s</span>
            <br />
            <script>document.write('<span class="field-clear-check-button pure-button pure-button-xsmall pure-button-error">Remove</span><span class="field-clear-cancel pure-button-xsmall pure-button pure-button-hidden">Cancel</span>')</script>
            <div class="browse-box">%(input)s</div>
    """
    template_with_clear = u"""
        <label for="%(clear_checkbox_id)s" class="field-clear-check">
            Remove file: %(clear)s (tick and save)
        </label>"""
    template_with_initial = u"""
        <div class="field-clear">
            %(input)s
            <noscript>%(clear_template)s</noscript>
            <script>document.write('<span class="field-clear-hidden-input pure-button pure-button-xsmall pure-button-hidden">%(clear)s</span>')</script>
        </div>"""
