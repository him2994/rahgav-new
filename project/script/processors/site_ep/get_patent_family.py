import os
import time



def get_patent_family(driver, number, directory, fetcher, saver,
        do_download, alias):
    
    base_patent = number.strip()

    driver.get("https://register.epo.org/regviewer?lng=en")
    driver.find_element_by_xpath('//*[@id="searchForm"]/div[1]/span[2]/textarea').clear()
    driver.find_element_by_xpath('//*[@id="searchForm"]/div[1]/span[2]/textarea').send_keys(base_patent)
    driver.find_element_by_xpath('//*[@id="searchForm"]/div[2]/div[2]/div[2]/div/span/input').click()
    base_patent_code = driver.current_url.strip().split("number=")[1]
    
    #download_script = 'downloadXML("/download?number=' + base_patent_code + '&tab=main&xml=st36", "")'
    if do_download:
        download_url = 'https://register.epo.org/download?number=' + base_patent_code + '&tab=main&xml=st36'
        filename = base_patent + ".xml"
        fetcher.download_file(download_url, os.path.join(directory, filename))
    
    patent_family = 'https://register.epo.org/application?number=' + base_patent_code + '&lng=en&tab=family'
    driver.get(patent_family)
    family_rows =  driver.find_elements_by_xpath('//*[@id="body"]/table/tbody/*')

    row_counter = 0
    # original_rows = 0
    publication = []
    pub_date = []
    pub_type = []
    priority = []
    prior_date = []
    pub_start = 0
    pri_start = 0
    type_group = ""
    for family_row in family_rows:
        # try:
            # print family_row.find_elements_by_tag_name('td')[0].text.strip()
        # except:
            # pass
        line_type = family_row.find_elements_by_tag_name('td')[0].text.strip()
        if line_type == "Type":
            type_group = family_row.find_elements_by_tag_name('td')[1].text.strip()
            row_counter = int(family_row.find_elements_by_tag_name('td')[0].get_attribute("rowspan"))
        if "Divisional application" in type_group:
            #print type_group
            saver.save_patent_family([alias, base_patent, type_group])
            type_group = ""
            continue
        #print(row_counter)
        if row_counter > 0:
            row_counter = row_counter - 1
            line_type = family_row.find_elements_by_tag_name('td')[0].text.strip()
            if line_type == "Publication No.":
                pub_start = 1
                continue
            if line_type == "Priority number":
                pub_start = 0
                pri_start = 1
                continue
            if pub_start == 1:
                publication.append(family_row.find_elements_by_tag_name('td')[0].text.strip())
                pub_date.append(family_row.find_elements_by_tag_name('td')[1].text.strip())
                pub_type.append(family_row.find_elements_by_tag_name('td')[2].text.strip())
            if pri_start == 1:
                priority.append(family_row.find_elements_by_tag_name('td')[0].text.strip())
                prior_date.append(family_row.find_elements_by_tag_name('td')[1].text.strip())
                
        if row_counter == 0:
            #print(type_group,publication,pub_date,pub_type,priority,prior_date)
            if len(publication) > 0:
                #saver.save_patent_family([base_patent, type_group, ";".join(publication), + ";".join(pub_date)])
                #saver.save_patent_family([";".join(pub_type), ";".join(priority), ";".join(prior_date)])
                saver.save_patent_family([alias, base_patent, type_group, ";".join(publication), ";".join(pub_date),
                    ";".join(pub_type), ";".join(priority), ";".join(prior_date)])
            publication = []
            pub_date = []
            pub_type = []
            priority = []
            prior_date = []
            pub_start = 0
            pri_start = 0
            type_group = ""
            row_counter = -1
    timer_set = 10
    timer = 0
    while timer < timer_set:
        #print(timer)
        time.sleep(5)
        timer = timer + 5

