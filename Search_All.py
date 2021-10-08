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
    tmp_link = link
    # link = "https://search.dcinside.com/post/q/.ED.96.89.EB.B3.B5"
    """페이지가 지정된 링크 :
        https://search.dcinside.com/post/p/1/q/.ED.96.89.EB.B3.B5
    """
    
    """페이지 수가 끝인지 아닌지 비교하기 위한 임시 string 변수"""
    tmp_str = ''
    
    """임시로 최대 200페이지까지 잡았지만 더 늘려도 OK. 아래 tmp_link는 입력한 링크 중간에 페이지 수를 끼워넣음"""
    for i in range(1, 200):
        tmp_link = link[:32]+"/p/"+str(i)+"/"+link[33:]

    #그 페이지의 html을 text로 가져온다.
        html_text = get(tmp_link).text

    # 그 html 내용을 좀 더 다루기 쉽게 BeautifulSoup로 만든다.
        soup = BeautifulSoup(html_text, 'lxml')
    # 원하는 url들이 있는 class를 찾는다.
        sch_list= soup.find_all('a', class_= 'tit_txt')
    # 그 안에서 링크만 쏙 빼오고 싶기 때문에 regular expression(정규 표현)을 사용한다.
        r = compile('href="(.*?)"')
    # for loop을 위해 비워둔 리스트
        url_list = []

        for link2 in sch_list:
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
            new_list.append(sub('&amp;', "&", url))
        
        """이전 페이지의 첫 번째 주소와 다음 페이지의 첫번째 주소가 동일하면 더 이상 페이지가 없는 것으로 간주하고 for문을 빠져나옴"""
        if(tmp_str == new_list[0]):
            break
        else:    
            tmp_str = new_list[0]

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