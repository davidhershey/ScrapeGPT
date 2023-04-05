
from typing import List, Tuple
import random
import copy
import re
from bs4 import BeautifulSoup
import requests

# This code to simplify the contents of a web page was taken from TaxyAI (https://github.com/TaxyAI/browser-extension)
# It was translated to Python with GPT-4 (prompt: "Translate this script from typescript to Python:")

TAXY_ELEMENT_SELECTOR = "data-taxy-element"

def is_interactive(element, style):
    return (
        element.name == "a"
        or element.name == "input"
        or element.name == "button"
        or element.name == "select"
        or element.name == "textarea"
        or element.has_attr("onclick")
        or element.has_attr("onmousedown")
        or element.has_attr("onmouseup")
        or element.has_attr("onkeydown")
        or element.has_attr("onkeyup")
        or style.get("cursor") == "pointer"
    )


def is_visible(element, style):
    return (
        style.get("opacity") != ""
        and style.get("display") != "none"
        and style.get("visibility") != "hidden"
        and style.get("opacity") != "0"
        and element.get("aria-hidden") != "true"
    )


current_elements = []


def traverse_dom(node, page_elements: List):
    cloned_node = copy.copy(node)
    # print(node.name)
    if isinstance(node, str):
        return {"pageElements": page_elements, "clonedDOM": cloned_node}

    if node.name is not None:
        style = {attr: node[attr] for attr in node.attrs if re.match(r"^style-", attr)}

        page_elements.append(node)
        cloned_node["data-id"] = str(len(page_elements) - 1)
        cloned_node["data-interactive"] = str(is_interactive(node, style))
        cloned_node["data-visible"] = str(is_visible(node, style))

        for child in node.children:
            result = traverse_dom(child, page_elements)
            cloned_node.append(result["clonedDOM"])

    return {"pageElements": page_elements, "clonedDOM": cloned_node}


def get_annotated_dom(html: str) -> Tuple[str, List]:
    global current_elements
    current_elements = []
    soup = BeautifulSoup(html, "html.parser")
    result = traverse_dom(soup.body, current_elements)
    return str(result["clonedDOM"]), current_elements


def get_unique_element_selector_id(idx: int) -> str:
    element = current_elements[idx]
    unique_id = element.get(TAXY_ELEMENT_SELECTOR)
    if unique_id:
        return unique_id
    unique_id = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=8))
    element[TAXY_ELEMENT_SELECTOR] = unique_id
    return unique_id

def get_simplified_dom(url):
    response = requests.get(url)
    full_dom, _ = get_annotated_dom(response.content)
    dom = BeautifulSoup(full_dom, "html.parser")

    interactive_elements = []

    simplified_dom = generate_simplified_dom(dom.body, interactive_elements)
    return simplified_dom.prettify()

def generate_simplified_dom(element, interactive_elements):
    from bs4.element import NavigableString

    if isinstance(element, NavigableString) and element.strip():
        return element.text[:int(len(element.text)/2)]
        # return element + ' '

    if not (element.name):
        return None

    # print(element.attrs)
    is_visible = element.attrs.get('data-visible') == 'True'
    if not is_visible:
        return None
    children = [generate_simplified_dom(c, interactive_elements) for c in element.children]
    children = [c for c in children if c is not None]
    

    if element.name == 'body':
        children = [c for c in children if not isinstance(c, str)]
        children = [c for c in children if not isinstance(c, NavigableString)]


    interactive = element.attrs.get('data-interactive') == 'True' or element.has_attr('role')
    has_label = element.has_attr('aria-label') or element.has_attr('name')
    include_node = interactive or has_label

    if not include_node and len(children) == 0:
        return None
    # if not include_node and len(children) == 1:
    #     return children[0]

    from bs4.element import Tag
    container = Tag(name=element.name)

    allowed_attributes = [
        'aria-label',
        'data-name',
        'name',
        'type',
        'placeholder',
        'value',
        'role',
        'title',
        'class',
        'id'
    ]

    for attr in allowed_attributes:
        if attr in element.attrs:
            container[attr] = element[attr]

    # if interactive:
    #     interactive_elements.append(element)
    #     container['id'] = element.get('data-id')

    for child in children:
        container.append(child)

    return container

if __name__ == "__main__":
    url = 'https://www.espn.com/nba/injuries'
    response = requests.get(url)
    simplified_html = get_simplified_dom(url)
    print(len(BeautifulSoup(response.content, "html.parser").prettify()))
    print(len(simplified_html.prettify()))
    with open('simplified.html', 'w') as f:
        f.write(simplified_html.prettify())
