# 내가 필요한 함수와 라이브러리를 import한다.
from bs4 import BeautifulSoup
from requests import get
from re import compile, findall, sub

# Just a function that turns lists into strings because the re.findall() really annoys me
def lststr(lst):
    string = ''
    return string.join(lst)

# 이 .py 파일을 실행하면 실행될 main method이다.
def main():
    # 혐오 표현을 "게시물 검색"으로 서치하면 나오는 결과 페이지 링크이다.
    link = input("DCINSIDE 혐오표현 검색 페이지 링크: ")
    #link = "https://search.dcinside.com/post/q/.ED.96.89.EB.B3.B5"
    
    """뽐뿌 사이트 예시(검색 키워드 : 강아지) :
    메인 페이지에서 바로 강아지 키워드를 검색했을 때 나오는 주소
    https://www.ppomppu.co.kr/search_bbs.php?keyword=%B0%AD%BE%C6%C1%F6
    """
    
    i = 1
    """모든 페이지의 검색 결과의 링크를 return 하는데 뽐뿌는 게시글 수가 천 단위가 넘길래...
    너무 내용이 많으면 while(1)을 while(i < 500) 정도로 바꾸세요
    그럼 500페이지까지의 링크를 출력합니다.
    이것도 너무 많으면 100으로 바꿔도 됩니다."""
    while(1):
        link = link + "&bbs_cate=2&search_type=sub_memo&order_typedate&page_no="+str(i)

    #그 페이지의 html을 text로 가져온다.
        html_text = get(link).text

    # 그 html 내용을 좀 더 다루기 쉽게 BeautifulSoup로 만든다.
        soup = BeautifulSoup(html_text, 'lxml')
    
        span_list = soup.findAll('span', class_ = 'title')
        
        if not span_list:
            break

    # 그 안에서 링크만 쏙 빼오고 싶기 때문에 regular expression(정규 표현)을 사용한다.
        r = compile('href="(.*?)"')
    # for loop을 위해 비워둔 리스트
        url_list = []

        for link2 in span_list:
        
        # re library는 string을 input으로 받아야하기 때문에 str()을 사용한다.
            link2 = str(link2)
        # re library를 사용해 링크 부분만 빼온다. 그러나 findall()은 list를 return한다. ㅂㄷㅂㄷ!!!
            url = r.findall(link2)
        # 그래서 아까 만들어둔 함수를 사용한다 ㅎ
            url_str = lststr(url)
        #비워둔 리스트에 추가해준다.
            url_list.append(url_str)

    #다른 사이트에서도 이런 문제가 발생하는 지는 모르겠지만, "&"가 "&amp;"로 바뀌어 가져와지는 현상이 일어났다.
    #그것도 고쳐주자. 안 그러면 링크가 먹통이다.
        new_list = []
    #링크에서 에러나는 부분들을 고쳐준다.
        for url in url_list:
            url = "https://www.ppomppu.co.kr"+url
            new_list.append(sub('&amp;', "&", url))

    # 제대로 모든 게 됐는 지 확인하는 for loop.
        for url in new_list:
            print(url)
        i += 1

    #url들을 txt파일에 저장한다.
        with open("url_list.txt", "w") as f:
            for url in new_list:
                f.write(url + "\n")
#이 파링을 실행하면 main method를 실행하도록 한다.
if __name__ == "__main__":
    main()