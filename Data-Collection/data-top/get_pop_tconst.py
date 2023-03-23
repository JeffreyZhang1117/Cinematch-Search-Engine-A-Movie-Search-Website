from functions import *
import json

# Prepare for page url (popular movies)
type_list = ["year=2010-01-01,2022-12-31"]
page_pre = "ref_=adv_prv"
page_nxt = "ref_=adv_nxt"
base_url = "https://www.imdb.com/search/title/?title_type=feature&languages=en"
home_url = "https://www.imdb.com"
start_url = "start="

# example0 = "https://www.imdb.com/search/title/?title_type=feature&year=2010-01-01,2021-12-31&ref_=adv_prv"
# example1 = "https://www.imdb.com/search/title/?title_type=feature&year=2010-01-01,2021-12-31&start=9951&ref_=adv_prv"
# example2 = "https://www.imdb.com/search/title/?title_type=feature&year=2010-01-01,2021-12-31&after=WzM4NDM2LCJ0dDcwNzM1MjIiLDEwMDAxXQ%3D%3D&ref_=adv_nxt"

# Get the url of each page (100 pages in all)
def get_pop_page_url(page_num):
    if page_num == 1:
        return base_url + '&' + type_list[0] + '&' + page_pre
    elif page_num > 1:
        num = 50 * (page_num - 1) + 1
        return base_url + '&' + type_list[0] + '&' + start_url + str(num) + '&' + page_nxt
    else:
        return "Wrong Page"


# Get the url of next page
def get_next_page_url(url):
      # return home_url + get_next_html(url)
    html_text = scrape_html(url)
    next = re.search('<a href="(.*?)"\nclass="lister-page-next next-page" >', html_text)
    if next:
        return home_url + next.group(1)

print(get_next_page_url('https://www.imdb.com/search/title/?title_type=feature&year=2010-01-01,2022-12-30&after=WzM3NDU3LDM3NDU3LCJ0dDE0MDA1MjUwIiwxMDAwMF0%3D&ref_=adv_nxt'))


# Get the top 100,000 movies' tconst
def get_all_pop_tconst2():
    all_tconst_list = []
    url = "https://www.imdb.com/search/title/?title_type=feature&year=2010-01-01,2022-12-31&start=1&ref_=adv_nxt"
    page_count = 0
    while page_count<2000:
        all_tconst_list.extend(get_tconst(url))
        url = get_next_page_url(url)
        page_count += 1
        print("Crawl Movie: " + str(50 * page_count))
    return all_tconst_list

def get_all_pop_info2():
    all_info_list = []
    url = "https://www.imdb.com/search/title/?title_type=feature&year=2010-01-01,2022-12-31&start=1&ref_=adv_nxt"
    page_count = 0
    while page_count<2000:
        all_info_list.extend(get_info50(url))
        url = get_next_page_url(url)
        page_count += 1
        print("Crawl Movie: " + str(50 * page_count))
    return all_info_list

def get_all_pop_tconst_info():
    all_tconst_list = []
    all_info_list = []
    web_add = []
    url = "https://www.imdb.com/search/title/?title_type=feature&year=2010-01-01,2022-12-31&start=1&ref_=adv_nxt"
    page_count = 0
    while page_count<2000:
        all_tconst_list.extend(get_tconst(url))
        all_info_list.extend(get_info50(url))
        url = get_next_page_url(url)
        page_count += 1
        if page_count > 200:
            web_add.append(url)
        print("Crawl Movie: " + str(50 * page_count))
    return all_tconst_list, all_info_list, web_add


# Output top 100,000 tconst to txt file
def output_pop_tconst():
    t_list = get_all_pop_tconst2()
    # clear file
    with open('data/pop_tconst.txt', 'w') as f:
        f.write('')

    # write tconst to file
    file = open('data/pop_tconst.txt', 'w')
    for i in range(len(t_list)):
        s = t_list[i] + "\n"
        file.write(s)
    file.close()

# Output top 100,000 info to txt file
def output_pop_info():
    info_list = get_all_pop_info2()
    # clear file
    with open('data/pop_info.txt', 'w') as f:
        f.write('')
    # write info to file
    file = open('data/pop_info.txt', 'w')
    for i in range(len(info_list)):
        s = json.dumps(info_list[i]) + "\n"
        file.write(s)
    file.close()

def output_pop_tconst_info():
    t_list, info_list,web_add = get_all_pop_tconst_info()
    # clear file
    with open('data/pop_tconst.txt', 'w') as f:
        f.write('')
    with open('data/pop_info.txt', 'w') as f:
        f.write('')

    with open('data/web_link.txt', 'w') as f:
        f.write('')
    # write tconst to file
    file = open('data/pop_tconst.txt', 'w')
    for i in range(len(t_list)):
        s = t_list[i] + "\n"
        file.write(s)
    file.close()
    # write info to file
    file = open('data/pop_info.txt', 'w')
    for i in range(len(info_list)):
        s = json.dumps(info_list[i]) + "\n"
        file.write(s)
    file.close()

    file = open('data/web_link.txt', 'w')
    for i in range(len(web_add)):
        s = web_add[i] + "\n"
        file.write(s)
    file.close()


if __name__ == '__main__':
    # pop_tconst = get_all_pop_tconst2()
    # print(pop_tconst)
    # output_pop_tconst()
    # print(1)
    # output_pop_info()
    # print(2)
    output_pop_tconst_info()

    # get_next_10k_info()

