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
    
    """디젤매니아 예시(검색 키워드 : 페미) :
    https://cafe.daum.net/_c21_/cafesearch?grpid=10akR&item=subject&sorttype=0&query=%ED%8E%98%EB%AF%B8#"""

    #그 페이지의 html을 text로 가져온다.
    html_text = get(link).text

    # 그 html 내용을 좀 더 다루기 쉽게 BeautifulSoup로 만든다.
    soup = BeautifulSoup(html_text, 'lxml')
    
    """ 디씨의 경우(기존 코드):

    # 원하는 url들이 있는 class를 찾는다.
    sch_list= soup.find_all('a', class_= 'tit_txt')

    디씨인사이드의 경우 'tit.txt' 태그가 먹히지만 다른 곳은 먹히지 않는다.
    
    디젤매니아의 경우 html 코드를 뜯어보면 <tr class='list_row_info'> 안에서 다시 한 번 td 태그로 들어가고, 거기서 a 태그를 추출한 뒤
    이후는 디씨에서 했던 것과 동일하게 정규식으로 href 태그에서 큰따옴표 안의 링크를 추출한다.
    구체적인 구조는 div id 'container' -> div id 'content' -> div class 'primary content' -> table 'class roundTable'
    -> tbody class 'pos_rel' -> form id 'innerSearchForm' -> table id 'searchCafeList' -> tr class 'list_row_info'다.
    
    BeautifulSoup에서 find로 td 태그의 id와 class 조건을 다는 것은 불가능하기 때문에 (soup.find('td', class_ = '클래스명') 불가능)
    리스트의 index를 이용하여 원하는 부분을 추출한다.
    """

    """다수의 tr 태그에 검색 결과가 저장되어 있기 때문에 findAll을 이용해 전체 검색 결과를 리스트에 담는다."""
    div_list = soup.findAll('tr', class_ = 'list_row_info')
    a_list=[]
    
    for link in div_list:
        tmp_list = link.findAll('td')
        str_tmp = tmp_list[1].find('a')
        a_list.append(str_tmp)
        
    """a_list는 기존 코드의 sch_list와 동일하다. 해당 리스트에 a 태그를 저장한다."""

    # 그 안에서 링크만 쏙 빼오고 싶기 때문에 regular expression(정규 표현)을 사용한다.
    r = compile('href="(.*?)"')
    # for loop을 위해 비워둔 리스트
    url_list = []

    for link in a_list:
        
        # re library는 string을 input으로 받아야하기 때문에 str()을 사용한다.
        link = str(link)
        # re library를 사용해 링크 부분만 빼온다. 그러나 findall()은 list를 return한다. ㅂㄷㅂㄷ!!!
        url = r.findall(link)
        # 그래서 아까 만들어둔 함수를 사용한다 ㅎ
        url_str = lststr(url)
        #비워둔 리스트에 추가해준다.
        url_list.append(url_str)

    #다른 사이트에서도 이런 문제가 발생하는 지는 모르겠지만, "&"가 "&amp;"로 바뀌어 가져와지는 현상이 일어났다.
    #그것도 고쳐주자. 안 그러면 링크가 먹통이다.
    new_list = []
    #링크에서 에러나는 부분들을 고쳐준다.
    for url in url_list:
        """디젤 매니아에서 추출한 <a href>의 경우 앞부분에 따로 주소를 붙여주어야 링크가 기능한다.
        참고로 카페에 가입해야 검색 결과를 볼 수 있기 때문에 가입 후 내용 체크가 가능하다."""
        url = "https://cafe.daum.net/"+url
        new_list.append(sub('&amp;', "&", url))

    # 제대로 모든 게 됐는 지 확인하는 for loop.
    for url in new_list:
        print(url)

    #url들을 txt파일에 저장한다.
    with open("url_list.txt", "w") as f:
        for url in new_list:
            f.write(url + "\n")
#이 파링을 실행하면 main method를 실행하도록 한다.
if __name__ == "__main__":
    main()
    
    
"""기본적으로 모든 웹페이지의 구조는 통일 되어 있지 않기 때문에 '보편적인 링크 추출기'는 힘들고, 
    찾아보고자 하는 페이지에 맞게 수정하는 과정이 필요하다.
    
    또한 현재 코드의 경우 1페이지의 검색 결과만을 보여주기 때문에(디씨인사이드, 디젤매니아 둘 다 포함) 다른 페이지의 결과를 찾고 싶다면
    for문을 이용하여 추출 과정을 반복하면 된다. 이때 디씨인사이드의 경우 페이지 주소의 중간 부분에  'p/1/', 'p/2/'등의 값을 넣어주어야
    하며, 아래 코드는 해당 반복 과정을 반영한 것.(디젤매니아는 검색 결과가 1페이지를 넘지 않아서 디씨인사이드로 지정.)
"""