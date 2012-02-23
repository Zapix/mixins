from django.forms.forms import BoundField
from django.utils.html import conditional_escape
from django.utils.encoding import StrAndUnicode, smart_unicode, force_unicode
from django.utils.safestring import mark_safe


class BootstrapBoundField(BoundField):
     def label_tag(self, contents=None, attrs=None):
        """
        Wraps the given contents in a <label>, if the field has an ID attribute.
        Adds for tag label class "control-label"
        """
        contents = contents or conditional_escape(self.label)
        widget = self.field.widget
        id_ = widget.attrs.get('id') or self.auto_id
        if id_:
            attrs = attrs and flatatt(attrs) or ''
            contents = u'<label class="control-label" for="%s"%s>%s</label>' % (widget.id_for_label(id_), attrs, unicode(contents))
        return mark_safe(contents)

class BootstrapFormMixin(object):
    
    def as_bootstrap(self):
        '''
        Returns form with bootstrap markup
        '''
        normal_row = u'<div class="control-group %(group_class)s">%(errors)s%(label)s<div class="controls"> %(field)s%(help_text)s</div></div>'
        error_row = u'<div>%s</div>'
        row_ender = u'</div>'
        help_text_html = u'<span class="help-inline">%s</span>'
        errors_on_separate_row = False
        
        top_errors = self.non_field_errors() # Errors that should be displayed above all fields.
        output, hidden_fields = [], []
        
        for name, field in self.fields.items():
            html_class_attr = ''
            group_class = ''
            bf = BootstrapBoundField(self, field, name)
            bf_errors = self.error_class([conditional_escape(error) for error in bf.errors]) # Escape and cache in local variable.
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend([u'(Hidden field %s) %s' % (name, force_unicode(e)) for e in bf_errors])
                hidden_fields.append(unicode(bf))
            else:
                # Create a 'class="..."' atribute if the row should have any
                # CSS classes applied.
                css_classes = bf.css_classes()
                if css_classes:
                    html_class_attr = ' class="%s"' % css_classes
                
                if bf_errors:
                    group_class = "error"

                if errors_on_separate_row and bf_errors:
                    output.append(error_row % force_unicode(bf_errors))

                if bf.label:
                    label = conditional_escape(force_unicode(bf.label))
                    # Only add the suffix if the label does not end in
                    # punctuation.
                    if self.label_suffix:
                        if label[-1] not in ':?.!':
                            label += self.label_suffix
                    label = bf.label_tag(label) or ''
                else:
                    label = ''

                if field.help_text:
                    help_text = help_text_html % force_unicode(field.help_text)
                else:
                    help_text = u''

                output.append(normal_row % {
                    'errors': force_unicode(bf_errors),
                    'group_class': group_class,
                    'label': force_unicode(label),
                    'field': unicode(bf),
                    'help_text': help_text,
                    'html_class_attr': html_class_attr
                })

        if top_errors:
            output.insert(0, error_row % force_unicode(top_errors))

        if hidden_fields: # Insert any hidden fields in the last row.
            str_hidden = u''.join(hidden_fields)
            if output:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and
                # insert the hidden fields.
                if not last_row.endswith(row_ender):
                    # This can happen in the as_p() case (and possibly others
                    # that users write): if there are only top errors, we may
                    # not be able to conscript the last row for our purposes,
                    # so insert a new, empty row.
                    last_row = (normal_row % {'errors': '', 'label': '',
                                              'field': '', 'help_text':'',
                                              'html_class_attr': html_class_attr})
                    output.append(last_row)
                output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
            else:
                # If there aren't any rows in the output, just append the
                # hidden fields.
                output.append(str_hidden)
        return mark_safe(u'\n'.join(output))
