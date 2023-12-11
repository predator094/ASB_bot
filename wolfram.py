import os
import requests
import wolframalpha
import streamlit as st
import urllib.request
from PIL import Image
from langchain.tools import tool


def link_to_image(url):
    img = Image.open(requests.get(url, stream=True).raw)
    # img = Image.open("gfg.png")
    return img


# os.environ["WOLFRAM_ALPHA_APPID"] = "RU4KTG-89WY6RY239"
# wolfram = WolframAlphaAPIWrapper()
# a=wolfram.run("What is 2x+5 = -3x + 7?")
# print(a )


class execute:
    def __init__(self):
        self.client = wolframalpha.Client("RU4KTG-89WY6RY239")

    def run(self, query: str):
        data = {}
        res = self.client.query(query)
        if res["@success"] == False:
            return "no information found"
        # for p in res.pods:
        #     for s in p.subpods:
        #         img = link_to_image(s.img["@src"])
        #         st.image(img)
        #         if s.plaintext != None:
        #             st.write(s.plaintext)
        #         data[s.plaintext] = s.img["@src"]

        # st.write(next(res.results))
        # print(next(res.results)["subpod"]["img"]["@src"])
        # st.write(next(res.results).text)
        # try:
        #     st.write(f"Asnwer:{next(res.results).text}\n")
        #     st.write(
        #         f"Image related to answer :{next(res.results)['subpod']['img']['@src']}"
        #     )
        # except StopIteration:
        #     pass
        if list(res.results) == []:
            return list(res.pods)
        else:
            return list(res.results)


wolfram = execute()
# wolfram.run("festival in india")
# execute(str("india"))
