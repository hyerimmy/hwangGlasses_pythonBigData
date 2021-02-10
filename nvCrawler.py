import os
import sys
import urllib.request
import datetime
import time
import json

client_id = 'qQzLdBLrgX38__G3RlUs'
client_secret = 'akgN0iUMMJ'


    
    
## [CODE1] : url 접속을 요청하고 응답을 받아 반환
def getRequestUrl(url):
    req = urllib.requeset.Request(url) #url에 대한 요청 보낼 객체 생성
    req.add_header("X-Naver-Client-Id", client_id) #API사용하기 위한 Client ID와 Client Secret 코드를 요청 객체 헤드에 추가
    req.add_header("X-Naver-Client-Secret", client_secret)
    
    try:
        response = urllib.request.urlopen(req) #요청객제에 대한 응답을 response 객체에 저장
        if response.getcode() == 200: #요청이 정상적으로 처리되었다면
            print("[%s] Url Requeset Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e: #요청이 처리되지 않은 예외상황이 발생하면
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

        
        
## [CODE2] : 네이버 뉴스 검색 url을 만들고 [CODE1]의 getRequestUrl(url)을 호출하여 반환받은 응답데이터를 파이썬 json 형식으로 반환
def getNaverSearch(node, srcText, page_start, display):
    base = "https://openapi.naver.com/v1/search"
    node = "/%s.json" % node
    parameters = "?query=%s%start=%s&display=%s"%(urllib.parse.quote(srcText), start, display)
    
    url = base + node + parameters
    responseDecode = getRequesetUrl(url) #[CODE1]
    
    if (responseDecode == None):
        return None
    else :
        return json.loads(responseDecode) #서버에서 받은 JSON형태의 응답 객체를 파이썬 객체로 로드하여 반환

    
    
##[CODE3] : JSON 형식의 응답 데이터를 필요한 항목만 정리하여 딕셔너리 리스트인 jsonResult를 구성하고 반환하도록 작성
def getPostData(post, jsonResult, cnt):
    #검색결과가 들어있는 post 객체에서 필요한 데이터 항목을 추출하여 변수에 저장
    title = post['title']
    description = post['description']
    org_link = post['originallink']
    link = post['link']
    
    pDate = datetime.datetime.strptime(post['pubDate'], '%a, %d %b %yY %H:%M:%S+0900')
    pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')
    
    jsonResult.append({'cnt':cnt, 'title':title, 'description':description, 'org_link':org_link, 'link':org_link, 'pDate':pDate})
    return



## [CODE0]
def main():
    node = 'news' #크롤링 할 대상
    srcText = input('검색어를 입력하세요 : ')
    cnt = 0 #검색결과 카운트
    jsonResult = [] #검색결과 저장할 리스트 객체
    
    jsonResponse = getNaverSearch(node, srcText, 1, 100) #[CODE2]
    totall = jsonResponse['total'] #전체검색결과개수
    
    while ((jsonResponse != None) and (jsonResponse['display'] != 0)) :
        for post in jsonResponse['items']:
            cnt += 1
            getPostData(post, jsonResult, cnt) #[CODE3] #검색결과하나씩처리하는작업
            
        start = jsonResponse['start'] + jsonResponse['display'] #다음 검색결과 100개를 가져오기 위해 start 위치 변경
        jsonResponse = getNaverSearch(node, srcText, start, 100) #새로운 검색 결과 jsonResponse에 저장
        
    print('전체검색 : %d 건' %total)
    
    with open('%s_naver_%s.json' % (srcText, node), 'w', encoding = 'utf8') as outfile :
        jsonFile = json.dumps(jsonResult, indent=4, sort_keys = True, ensure_ascii = False)
        
        outfile.write(jsonFile)
        
    print("가져온 데이터 : %d 건" %(cnt))
    print('%s_naver_%s.json SAVED' % (srcText, node))
    
if __name__=='__main__' :
    main()
