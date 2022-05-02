class URL :
    base_url = 'https://map.naver.com/v5/search/{placeName}/place'

class Selector:
    # kakao search

    # get place info
    informationSelector = '#app-root > div > div > div > div:nth-child({num}) > div > div.place_section.no_margin._18vYz > div > ul > li'

    # get review

class XPath :
    ## kakao search
    search_path_kakao = '//*[@id="search.keyword.query"]'

    # get place info
    searchIframe = '//*[@id="searchIframe"]'
    entryIframe = '//*[@id="entryIframe"]'
    first_fetched = '//*[@id="_pcmap_list_scroll_container"]/ul/li[1]/div[1]/a[1]'
    menu_tab_path = '//*[@id="app-root"]/div/div/div/div[4]/div/div/div/div/a[{num}]'
    menuTab2Path = '//*[@id="app-root"]/div/div/div/div[4]/div/div/div/div/div/div[2]/div/div/a[{num}]/span'
    menuTab3Path = '//*[@id="root"]/div[2]/div/header/div[2]/div/a[{num}]/span'
    menuMoreButton = '//*[@id="app-root"]/div/div/div/div[6]/div/div[1]/div[2]/a'

    placeMeanRating = '//*[@id="app-root"]/div/div/div/div[2]/div[1]/div[2]/span[1]/em'
    serviceHour = '//*[@id="app-root"]/div/div/div/div[5]/div/div[1]/div/ul/li[4]/div/a'
    summary = '//*[@id="app-root"]/div/div/div/div[5]/div/div[1]/div/ul/li[4]/div/a'
    agePopluarity = '//*[@id="bar_chart_container"]/ul/li[{age}]/div[1]/span/span'
    femalePopularity = '//*[@id="_datalab_chart_donut1_0"]/svg/g[1]/g[3]/g[4]/g[2]/text[2]/text()'
    malePopularity = '//*[@id="_datalab_chart_donut1_0"]/svg/g[1]/g[3]/g[4]/g[2]/text[1]'
    telephone = '//*[@id="app-root"]/div/div/div/div[5]/div/div[1]/div/ul/li[1]/div/span[1]'
    likeMorePath = '/html/body/div[3]/div/div/div/div[5]/div[3]/div[1]/div/div/div[2]/a'

    reviewPath = '//*[@id="app-root"]/div/div/div/div[4]/div/div/div/div/a[3]/span'
    timePath = '//*[@id="app-root"]/div/div/div/div[5]/div/div[1]/div/ul/li[4]/div/a/div/div/span'


    placeName = '//*[@id="_title"]/span[1]'
    placeType = '//*[@id="_title"]/span[2]'
    timeMoreButton = '//*[@id="app-root"]/div/div/div/div[5]/div/div[{div_num}]/div/ul/li[{idx}]/div/a/div/div/span'
    timeMoreButton2 = '//*[@id="app-root"]/div/div/div/div[6]/div/div[{div_num}]/div/ul/li[{idx}]/div/a/div[1]/div/span'

    descriptionMoreButton = '//*[@id="app-root"]/div/div/div/div[5]/div/div[{div_num}]/div/ul/li[{idx}]/div/a/span[2]'
    descriptionMoreButton2 = '//*[@id="app-root"]/div/div/div/div[6]/div/div[{div_num}]/div/ul/li[{idx}]/div/a/span[2]'

    description = '//*[@id="app-root"]/div/div/div/div[{div_num1}]/div/div[{div_num2}]/div/ul/li[{idx}]/div/a/span[1]'
    infoText = '//*[@id="app-root"]/div/div/div/div[5]/div/div[{div_num}]/div/ul/li[{idx}]/div/a/span[1]'
    datalabMoreButton = '//*[@id="app-root"]/div/div/div/div[6]/div/div[{div_num}]/div[2]/a'

    reviewNum = '//*[@id="app-root"]/div/div/div/div[2]/div[1]/div[2]/span[{num}]/a/em'
    placeTab = '//*[@id="app-root"]/div/div/div/div[4]/div/div/div/div'
    homePath = '//*[@id="app-root"]/div/div/div/div[4]/div/div/div/div/a[1]/span'

    # get review


class ClassName :
    # kakao search

    # get place info
    menuClass = '_2kAri'
    menuListClass = '_3yfZ1'
    menuPriceClass = '_3qFuX'

    themeKeywordClass = 'Z6Prg'
    themeTopicClass = '_3hvd9'
    themeDataClass = '_2irYJ'
    descriptionClass = 'M_704'
    popularityClass = '_3QHlQ'

    placeMeanRatingClass = '_2XLwD'
    telephoneClass = '_3ZA0S'
    placeAddressClass = '_2yqUQ'
    likeTopicClass = '_1lntw'
    likeNumClass = 'Nqp-s'
    likeMoreClass = '_22igH'

    dayClass = '_1v6gO'
    timeClass = '_3uEtO'
    timeMoreButtonClass = '_1aKLL'

    descriptionMoreButtonClass = '_3_09q'
    zeroClass = '_13OJC'
    announcementClass = '_3puAz'

    deliveryClass = '_3eMEwPl5IJ'
    deliveryMenuNameClass = 'name'
    deliveryMenuPriceClass = 'price'

    takeoutClass = 'desc_type ico_takeout'
    takeOutMenuNameClass = 'tit'

    femaleClass = 'c3-chart-arc c3-target c3-target-female'

    donutGraphClass = 'c3-chart'

    # get review
