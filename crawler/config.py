class Path:
    baseURL = 'https://map.naver.com/v5/search/{placeName}/place'
    searchIframe = '//*[@id="searchIframe"]'
    entryIframe = '//*[@id="entryIframe"]'
    firstFetched = '//*[@id="_pcmap_list_scroll_container"]/ul/li[1]/div[2]/a[1]'
    placeName = '//*[@id="_title"]/span[1]'
    placeAddress = '//*[@id="app-root"]/div/div/div/div[5]/div/div[1]/div/ul/li[2]/div/a/span[1]'
    visitorReview = ''

    serviceHour = '//*[@id="app-root"]/div/div/div/div[5]/div/div[1]/div/ul/li[4]/div/a'
    summary = '//*[@id="app-root"]/div/div/div/div[5]/div/div[1]/div/ul/li[4]/div/a'
    menuButton = '//*[@id="app-root"]/div/div/div/div[4]/div/div/div/div/a[2]'
