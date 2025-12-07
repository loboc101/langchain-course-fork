from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

load_dotenv()


def main():
    print("Hello from langchain-course!")
    information = """
    Grace Elizabeth Gold (born August 17, 1995), known as Gracie Gold,[2] is an American figure skater. She is a 2014 Olympic bronze medalist in the team event, a six-time Grand Prix medalist (2 gold, 2 silver, 2 bronze), and a two-time U.S. national champion (2014, 2016). She placed 4th at the 2014 Winter Olympics in Sochi, Russia. At the junior level, Gold is the 2012 World Junior silver medalist, the 2011 JGP Estonia champion, and the 2012 U.S. junior national champion.

    In 2014, Gold became the first American woman to win the NHK Trophy title on the Grand Prix Series circuit and holds the record for the highest short program score ever recorded by an American woman (76.43) which she achieved at the 2016 World Championships in Boston. She is a mental health advocate and was recognized with the 2022 Bell of Hope Award. She was featured in the HBO sports documentary The Weight of Gold (2020), and her memoir Outofshapeworthlessloser: A Memoir of Figure Skating, F*cking Up, and Figuring It Out released in February 2024, was on the New York Times Bestseller list.
    Grace Elizabeth Gold was born on August 17, 1995, in Newton, Massachusetts.[3] She is the daughter of Denise, an ER nurse, and Carl Gold, an anesthesiologist.[4][5] Gracie's fraternal twin sister, Carly Gold (named after their father), is younger by 40 minutes and also competed in figure skating.[6][7]

    Gold grew up in Springfield, Missouri before she and her family moved to Springfield, Illinois.[4] She said that she has lived in Corpus Christi, Texas.[8] She attended ninth grade at Glenwood High School in Chatham, Illinois, before switching to online education through the University of Missouri.[5][9] She has taken ballet lessons to improve her performance in skating.[10]
    """

    summary_template = """
    given the information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOllama(temperature=0.5, model="gemma3:270m")
    # llm = ChatOpenAI(temperature=0, model="gpt-5-nano")
    
    # chain = summary_prompt_template | llm
    # response = chain.invoke(input={"information": information})

    story_template = PromptTemplate(
        input_variables=["theme"],
        template="Write a short poem about: {theme}"
    )
    chain = story_template | llm
    response = chain.invoke(input={"theme": "Gracie, a skater overcoming adversity"})

    print(response.content)

if __name__ == "__main__":
    main()