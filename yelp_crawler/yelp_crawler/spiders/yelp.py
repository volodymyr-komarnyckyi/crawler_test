import scrapy


class YelpSpider(scrapy.Spider):
    name = "yelp"

    def start_requests(self):
        business_type = input("Введіть тип бізнесу (наприклад, restaurants): ")
        location = input("Введіть локацію (наприклад, New York, NY): ")

        start_url = (
            f"https://www.yelp.com/search?find_desc={business_type}&find_loc={location}"
        )

        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        businesses = response.css(".css-1qn0b6x")

        for business in businesses:
            yield {
                "Business name": business.css(".css-1agk4wl a::text").get(),
                "Rating": business.css(
                    "div[aria-label*=rating]::attr(aria-label)"
                ).get(),
                "Number of reviews": business.css(
                    "span.reviewCount__09f24__EUXPN::text"
                ).get(),
                "Yelp URL": response.urljoin(
                    business.css(".css-1agk4wl a::attr(href)").get()
                ),
                "Business website": business.css(
                    'a[rel="noopener nofollow"]::attr(href)'
                ).get(),
                "List of first 5 reviews": [
                    {
                        "Reviewer name": review.css(".css-1pzprxn a::text").get(),
                        "Reviewer location": review.css(".css-dfcb2b::text").get(),
                        "Review date": review.css(".css-e81eai::text").get(),
                    }
                    for review in business.css(".css-79elbk")
                ],
            }

        next_page = response.css(".css-1h75h8t::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
