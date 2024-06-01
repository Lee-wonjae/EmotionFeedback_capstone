from langchain.schema import BaseOutputParser

class CommaOutputParser(BaseOutputParser):
    def parse(self,text):
        items=text.strip().split(",")
        return list(map(str.strip,items))