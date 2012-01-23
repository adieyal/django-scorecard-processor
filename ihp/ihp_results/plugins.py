from scorecard_processor.plugins.input.multi_choices import register, MultiChoiceField

class AidTypes(MultiChoiceField):
    def __init__(self, *args, **kwargs):
        super(AidTypes,self).__init__(*args, **kwargs)
        self.choices = (
            ('financial','Financial support'),
            ('technical','Technical assistance (non-financial)'),
            ('lobbying','Lobbying/advocay - non-financial')
        )
        self.widget.choices = self.choices

register.register('input','IHP field','aid_types', AidTypes)

