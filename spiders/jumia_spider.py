import scrapy


class JumiaSpiderSpider(scrapy.Spider):
    name = "jumia_spider"
    allowed_domains = ["www.jumia.ug"]
    start_urls = ["https://www.jumia.ug/catalog/?q=smartwatches"]

    def parse(self, response):
        nxt_url = None
        products_ctn = response.css("div.-paxs")
        products = products_ctn.css("article")
        pdt_count = len(products)

        nxt_pg_div = response.css("div.pg-w")
        nxt_pgs = nxt_pg_div.css("a")
        nxt_link = nxt_pgs.css("[aria-label='Next Page']").attrib["href"]

        if nxt_link!=None:
            nxt_url = "https://www.jumia.ug"+nxt_link
        for product in products:
            product_ctn = product.css("a")
            pdt_info = product_ctn.css("div.info")
            pdt_name = pdt_info.css("h3.name::text").get()
            pdt_price = pdt_info.css("div.prc::text").get()
            yield{"pdt_name":pdt_name,"pdt_price":pdt_price,"pdt_count":pdt_count,"nxt":nxt_url}

        #print(products)
        
        yield products

        #nxt_pg_div = response.css("div.pg-w")
        #nxt_pgs = nxt_pg_div.css("a")
        #nxt_link = nxt_pgs.css("[aria-label='Next Page']").attrib["href"]
        
        if nxt_link is not None:
            nxt_url = "https://www.jumia.ug"+nxt_link
            yield response.follow(nxt_url,callback=self.parse)
        pass