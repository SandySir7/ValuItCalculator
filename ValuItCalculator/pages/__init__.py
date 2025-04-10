# This makes the pages directory a Python package
# and enables importing modules from it

# Import all page modules to make them accessible from pages
from .about import show as about_show
from .company_info import show as company_info_show
from .faq import show as faq_show
from .home import show as home_show
from .learn import show as learn_show
from .my_valuations import show as my_valuations_show
from .professional_mode import show as professional_mode_show
from .valuation_tool import show as valuation_tool_show

# Create aliases for the imported show functions
home = home_show
valuation_tool = valuation_tool_show
my_valuations = my_valuations_show
professional_mode = professional_mode_show
learn = learn_show
company_info = company_info_show
about = about_show
faq = faq_show