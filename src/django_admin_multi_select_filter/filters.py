from django.contrib import admin
from django.contrib.admin.utils import reverse_field_path
from django.utils.translation import gettext_lazy as _


class MultiSelectFieldListFilter(admin.FieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = field_path + "__in"
        self.lookup_kwarg_isnull = field_path + "__isnull"

        super().__init__(field, request, params, model, model_admin, field_path)

        self.lookup_val = self.used_parameters.get(self.lookup_kwarg, [])
        if len(self.lookup_val) == 1 and self.lookup_val[0] == "":
            self.lookup_val = []
        self.lookup_val_isnull = self.used_parameters.get(self.lookup_kwarg_isnull)

        self.empty_value_display = model_admin.get_empty_value_display()
        parent_model, reverse_path = reverse_field_path(model, field_path)
        # Obey parent ModelAdmin queryset when deciding which options to show
        if model == parent_model:
            queryset = model_admin.get_queryset(request)
            self.lookup_choices = (
                queryset.distinct().order_by(field.name).values_list(field.name, flat=True)
            )
        else:
            queryset = parent_model._default_manager.all()
            self.lookup_choices = queryset.distinct()
            
    def expected_parameters(self):
        return [self.lookup_kwarg, self.lookup_kwarg_isnull]

    def choices(self, changelist):
        yield {
            "selected": not self.lookup_val and self.lookup_val_isnull is None,
            "query_string": changelist.get_query_string(
                remove=[self.lookup_kwarg, self.lookup_kwarg_isnull]
            ),
            "display": _("All"),
        }
        include_none = False
        for val in self.lookup_choices:
            if val is None:
                include_none = True
                continue
            val = str(val)

            if val in self.lookup_val:
                values = [v for v in self.lookup_val if v != val]
            else:
                values = self.lookup_val + [val]

            if values:
                yield {
                    "selected": val in self.lookup_val,
                    "query_string": changelist.get_query_string(
                        {self.lookup_kwarg: ",".join(values)},
                        [self.lookup_kwarg_isnull],
                    ),
                    "display": val,
                }
            else:
                yield {
                    "selected": val in self.lookup_val,
                    "query_string": changelist.get_query_string(
                        remove=[self.lookup_kwarg]
                    ),
                    "display": val,
                }

        if include_none:
            yield {
                "selected": bool(self.lookup_val_isnull),
                "query_string": changelist.get_query_string(
                    {self.lookup_kwarg_isnull: "True"}, [self.lookup_kwarg]
                ),
                "display": self.empty_value_display,
            }
