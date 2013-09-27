
from piston.utils import rc
from piston.handler import BaseHandler

from colab.deprecated import solrutils


class SearchHandler(BaseHandler):
    allowed_methods = ('GET', )

    def read(self, request):
        query = request.GET.get('q')
        page = request.GET.get('p', 1)
        results_per_page = request.GET.get('n', 50)
        order = request.GET.get('o')

        if not query:
            return 'Query cannot be empty.'
        else:
            query = query.encode('utf-8')

        try: 
            n = int(results_per_page)
        except ValueError:
            n = 10
    
        if 1 > n > 500:
            n = 1
        
        try:
            page = int(page)
        except ValueError:
            page = 1
        
        if page < 1:
            page = 1

        return solrutils.select(query, results_per_page, page, order)
