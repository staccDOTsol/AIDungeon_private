import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


"""
format of tree is
dict {
    tree_id: tree_id_text
    context: context text?
    first_story_block
    action_results: [act_res1, act_res2, act_res3...]
}

where each action_result's format is:
dict{
    action: action_text
    result: result_text
    action_results: [act_res1, act_res2, act_res3...]
}
"""


class Scraper:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.max_depth = 10
        self.end_actions = {
            "End Game and Leave Comments",
            "Click here to End the Game and Leave Comments",
            "See How Well You Did (you can still back-page afterwards if you like)",
            "You have died.",
            "You have died",
            "Epilogue",
            "Save Game",
            "Your quest might have been more successful...",
            "5 - not the best, certainly not the worst",
            "The End! (leave comments on game)",
            "6 - it's worth every cent",
            "You do not survive the journey to California",
            "Quit the game.",
            "7 - even better than Reeses' Cups®",
            "8 - it will bring you enlightenment",
            "End of game! Leave a comment!",
            "Better luck next time",
            "click here to continue",
            "Rating And Leaving Comments",
            "You do not survive your journey to California",
            "Your Outlaw Career has come to an end",
            "Thank you for taking the time to read my story",
            "You have no further part in the story, End Game and Leave Comments",
            "",
            "You play no further part in this story. End Game and Leave Comments",
            "drivers",
            "Alas, poor Yorick, they slew you well",
            "My heart bleeds for you",
            "To End the Game and Leave Comments click here",
            "Call it a day",
            "Check the voicemail.",
            "reset",
            "There's nothing you can do anymore...it's over.",
            "To Be Continued...",
            "Thanks again for taking the time to read this",
            "If you just want to escape this endless story you can do that by clicking here",
            "Boo Hoo Hoo",
            "End.",
            "Pick up some money real quick",
            "",
            "Well you did live a decent amount of time in the Army",
            "End Game",
            "You have survived the Donner Party's journey to California!",
        }
        self.texts = set()
    def close(self):
        self.driver.close()
    def GoToURL(self, url):
        self.texts = set()
        self.driver.get(url)
        time.sleep(0.5)

    def GetText(self):
        div_elements = self.driver.find_elements_by_css_selector("div")
        text = div_elements[3].text
        return text

    def GetLinks(self):
        return self.driver.find_elements_by_css_selector("a")

    def GoBack(self):
        self.GetLinks()[0].click()
        time.sleep(0.2)

    def ClickAction(self, links, action_num):
        links[action_num + 4].click()
        time.sleep(0.2)

    def GetActions(self):
        return [link.text for link in self.GetLinks()[4:]]

    def NumActions(self):
        return len(self.GetLinks()) - 4

    def BuildTreeHelper(self, parent_story, action_num, depth, old_actions):
        depth += 1
        action_result = {}

        action = old_actions[action_num]
        print("Action is ", repr(action))
        action_result["action"] = action

        links = self.GetLinks()
        if action_num + 4 >= len(links):
            return None

        self.ClickAction(links, action_num)
        result = self.GetText()
        if result == parent_story or result in self.texts:
            self.GoBack()
            return None

        self.texts.add(result)
        print(len(self.texts))

        action_result["result"] = result

        actions = self.GetActions()
        action_result["action_results"] = []

        for i, action in enumerate(actions):
            if actions[i] not in self.end_actions:
                sub_action_result = self.BuildTreeHelper(result, i, depth, actions)
                if action_result is not None:
                    action_result["action_results"].append(sub_action_result)

        self.GoBack()
        return action_result

    def BuildStoryTree(self, url, scraper):
        scraper.GoToURL(url)
        text = scraper.GetText()
        actions = self.GetActions()
        story_dict = {}
        story_dict["tree_id"] = url
        story_dict["context"] = ""
        story_dict["first_story_block"] = text
        story_dict["action_results"] = []

        for i, action in enumerate(actions):
            if action not in self.end_actions:
                action_result = self.BuildTreeHelper(text, i, 0, actions)
                if action_result is not None:
                    story_dict["action_results"].append(action_result)
            else:
                print("done")

        return story_dict


def save_tree(tree, filename):
    with open(filename, "w") as fp:
        json.dump(tree, fp)


urls = ['http://chooseyourstory.com/story/viewer/default.aspx?StoryId=11246', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=13454', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=56515', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=7480', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=28030', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=10359', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=4477', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=60010', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=64216', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=34193', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=7567', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=11730', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=4361', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=56622', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=43573', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=38891', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=61749', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=61316', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=8097', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=45629', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=56514', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=1447', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=38025', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=63471', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=62471', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=60933', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=38276', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=51930', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=45304', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=54001', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=12030', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=63463', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=34604', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=53243', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=56507', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=13274', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=7817', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=6606', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=36396', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=4139', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=23864', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=56522', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=26146', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=25338', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=10160', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=64451', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=9902', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=49642', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=31877', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=11968', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=13398', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=1046', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=4072', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=8716', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=62789', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=23389', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=5296', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=23381', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=10516', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=17736', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=48337', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=51301', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=23419', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=29596', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=61409', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=17721', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=34885', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=9898', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=13423', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=29025', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=18729', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=57269', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=41237', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=9770', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=23324', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=45288', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=23343', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=13659', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=7565', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=16215', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=30252', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=38933', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=44170', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=16070', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=23012', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=16263', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=2320', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=54187', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=7374', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=32087', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=33092', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=30375', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=64885', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=60383', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=45314', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=21917', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=10933', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=59531', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=61040', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=53953', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=996', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=38975', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=26469', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=27023', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=33006', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=8936', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=21343', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=7965', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=11142', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=26441', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=62617', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=18800', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=54019', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=26739', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=11797', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=46643', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=226', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=34679', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=11147', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=7560', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=9993', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=44834', 'http://chooseyourstory.com/story/viewer/default.aspx?StoryId=23165']

import threading

def doIt(i):
    scraper = Scraper()
    tree = scraper.BuildStoryTree(urls[i], scraper)
    save_tree(tree, "stories/story" + str(41 + i) + ".json")
    scraper.close()

for i in range(0, len(urls)):
    print("****** Extracting Adventure ", urls[i], " ***********")
    t = threading.Thread(target=doIt, args=(i,))
    t.daemon = True 
    t.start()
    time.sleep(1)
    while threading.active_count() > 8:
        time.sleep(1)
        print(threading.active_count())
print("done")
