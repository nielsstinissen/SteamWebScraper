# -*- coding: utf-8 -*-
import scrapy


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com/search/?specials=1']

    def parse(self, response):
        all_games = response.xpath('//body/div/div[@class="responsive_page_content"]/div[@class="responsive_page_template_content"]/form/div/div/div/div[@class="search_results"]/div[@id="search_result_container"]/div[@id="search_resultsRows"]/a')

        for game in all_games:
            #getting link
            link = self.start_urls[0] + game.xpath('.//@href').extract_first()

            #getting title
            title = game.xpath('.//div[@class="responsive_search_name_combined"]/div[1]/span/text()').extract_first()

            #getting release_date
            release_date = game.xpath('.//div[@class="responsive_search_name_combined"]/div[2]/text()').extract_first()
            if release_date is None:
                release_date = 0

            #getting reviewscore
            review = game.xpath('.//div[@class="responsive_search_name_combined"]/div[3]/span/@class').extract_first()
            if review is not None:
                #look wich reviewscore the game has
                review_score = ""
                if "positive" in review:
                    review_score = "postive"
                elif "mixed" in review:
                    review_score = "mixed"
                elif "negative" in review:
                    review_score = "negative"
                else:
                    review_score = "unkown"
            else:
                review = 0

            #getting the discount
            discount_before = game.xpath('.//div[@class="responsive_search_name_combined"]/div[4]/div/span/text()').extract_first()

            #erasing - and %
            discount = ""
            if discount_before is not None:
                discount = discount_before[1:-1]

            else:
                discount = 0


            #getting old_price
            old_price_before = game.xpath('.//div[@class="responsive_search_name_combined"]/div[4]/div[2]/span/strike/text()').extract_first()

            #Test for the type of valuta
            if old_price_before is not None:
                valuta = ""
                if "€" in old_price_before:
                    valuta == "€"
                elif "$" in old_price_before:
                    valuta == "$"
                elif "£" in old_price_before:
                    valuta == "£"
                else:
                    valuta == "unkown"

                #remove valuta and change , to . so it can be seen as an float
                old_price = old_price_before[:-1]
                old_price = old_price.replace(',','.')


            else:
                old_price = 0

            #calculate new_price because we can't scrape it from the site
            discount_price = (float(old_price) * int(discount)) / 100
            new_price = float(old_price) - float(discount_price)
            new_price = ("%.3f" % new_price)
            new_price = new_price[0:-1]

            yield {
                'title': title,
                'release_date': release_date,
                'review_score': review_score,
                'old_price': old_price,
                'new_price': new_price,
                'link': link,
            }