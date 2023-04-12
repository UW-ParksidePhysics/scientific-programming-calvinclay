def scrape_web_data(url):
    import pandas as pd

    url_data = pd.read_html(url)
    return url_data








if __name__ == '__main__':
    gas_data_url = 'https://www.ohio.edu/mechanical/thermo/property_tables/gas/idealGas.html'
