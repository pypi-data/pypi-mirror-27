#!/usr/bin/env GoodTests.py
'''
    Test various attribute related things
'''

import sys
import subprocess

from AdvancedHTMLParser.Tags import AdvancedTag
from AdvancedHTMLParser.Parser import AdvancedHTMLParser
from AdvancedHTMLParser.SpecialAttributes import StyleAttribute


class TestAttributes(object):
    '''
        Tests some attribute behaviour
    '''

    def test_setAttribute(self):
        tag = AdvancedTag('div')

        tag.setAttribute('id', 'abc')

        assert tag.getAttribute('id') == 'abc' , 'Expected id to be abc'

        assert tag.getAttribute('blah') == None , 'Expected unset attribute to return None, actually returned %s' %(tag.getAttribute('blah'),)

    def test_getElementsByAttr(self):
        html = """<html> <head> <title> Hello </title> </head>
<body>
    <div cheese="cheddar" id="cheddar1" >
        <span> Hello </span>
    </div>
    <div cheese="bologna" id="not_really_cheese">
        <span cheese="cheddar" id="cheddar2" > Goodbye </span>
    </div>
</body>
</html>"""
        parser = AdvancedHTMLParser()
        parser.parseStr(html)

        elements = parser.getElementsByAttr('cheese', 'cheddar')
        assert len(elements) == 2
        
        foundCheese1 = foundCheese2 = False
        for element in elements:
            myID = element.getAttribute('id')
            if myID == 'cheddar1':
                foundCheese1 = True
            elif myID == 'cheddar2':
                foundCheese2 = True

        assert foundCheese1
        assert foundCheese2


    def test_getAttributesList(self):
        parser = AdvancedHTMLParser()

        parser.parseStr('<div id="hello" style="display: none; width: 500px; padding-left: 15px;" class="One Two" data="Yes">Hello</div>')

        helloEm = parser.getElementById('hello')

        assert helloEm.getAttribute('id', '') == 'hello' , 'Got unxpected element'

        attributesList = helloEm.getAttributesList()

        foundId = False
        foundStyle = False
        foundClass = False
        foundData = False

        for attrName, attrValue in attributesList:
            if attrName == 'id':
                assert attrValue == 'hello' , 'Attribute "id" did not have expected value "hello", got "%s"' %(attrValue,)

                foundId = True
            elif attrName == 'style':
                
                style = StyleAttribute(attrValue)
                assert style.display == 'none', 'Got unexpected value for display in style copy. Expected "none", got "%s"' %(style.display,)
                assert style.width == '500px' , 'Got unexpected value for width in style copy. Expected "500px", got "%s"' %(style.width,)
                assert style.paddingLeft == '15px', 'Got unexpected value for padding-left. Expected "15px", got "%s"' %(style.paddingLeft, )
                
                foundStyle = True
            elif attrName == 'class':

                assert attrValue == 'One Two', 'Expected class name to equal "One Two", got: %s' %(attrValue, )

                foundClass = True
            elif attrName == 'data':

                assert attrValue == 'Yes', 'Expected attribute "data" to have the value "Yes", got: %s' %(attrValue, )

                foundData = True

            else:
                raise AssertionError('Got unexpected attribute in copy: (%s, %s)' %(attrName, attrValue))


        assert foundId is True , 'Did not find id element in attribute list'
        assert foundStyle is True , 'Did not find style element in attribute list'
        assert foundClass is True , 'Did not find class element in attribute list'
        assert foundData is True , 'Did not find data element in attribute list'

        # Test that we have a COPY, not the originals

        for item in attributesList:
            if item[0] == 'style':
                # Just incase in the future we want to include a StyleAttribute instead of the str
                if not isinstance(item[1], StyleAttribute):
                    style = StyleAttribute(item[1])
                else:
                    style = item[1]
                style.paddingTop = '10px'


        
        # These should not be modified in the original element
        assert 'padding-top' not in str(helloEm.style)
#        parser.parseStr('<div id="hello" style="display: none; width: 500px; padding-left: 15px;" class="One Two" data="Yes">Hello</div>')

    def test_getAttributesDict(self):
        parser = AdvancedHTMLParser()

        parser.parseStr('<div id="hello" style="display: none; width: 500px; padding-left: 15px;" class="One Two" data="Yes">Hello</div>')

        helloEm = parser.getElementById('hello')

        assert helloEm.getAttribute('id', '') == 'hello' , 'Got unxpected element'

        attributesDict = helloEm.getAttributesDict()

        assert 'id' in attributesDict , 'Did not find "id" in the attributes dict copy'
        assert 'style' in attributesDict , 'Did not find "style" in the attributes dict copy'
        assert 'class' in attributesDict , 'Did not find "class" in the attributes dict copy'
        assert 'data' in attributesDict , 'Did not find "data" in the attributes dict copy'

        assert len(attributesDict.keys()) == 4 , 'Got unexpected keys in attributesDict. Only expected "id" "style" "class" and "data", got: "%s"' %(repr(attributesDict),)

        assert attributesDict['id'] == 'hello' , 'Attribute "id" did not have expected value "hello", got "%s"' %(attributesDict['id'],)

        style = StyleAttribute(attributesDict['style'])
        assert style.display == 'none', 'Got unexpected value for display in style copy. Expected "none", got "%s"' %(style.display,)
        assert style.width == '500px' , 'Got unexpected value for width in style copy. Expected "500px", got "%s"' %(style.width,)
        assert style.paddingLeft == '15px', 'Got unexpected value for padding-left. Expected "15px", got "%s"' %(style.paddingLeft, )

        assert attributesDict['class'] == 'One Two', 'Got unexpected value for "class" in dict copy. Expected "One Two", Got: "%s"' %(attributesDict['class'], )

        assert attributesDict['data'] == 'Yes' , 'Got unexpected value for "data" in dict copy, Expected "Yes", Got: "%s"' %(attributesDict['data'], )

        # Assert we aren't modifying the original element
        style.paddingTop = '13em'

        assert helloEm.style.paddingTop != '13em' , 'Expected getAttributesDict to return copies, but modified original element on "style"'

        attributesDict['class'] += ' Three'

        assert 'Three' not in helloEm.getAttribute('class') , 'Expected getAttributesDict to return copies, but modified original element on "class"'

        attributesDict['id'] = 'zzz'

        assert helloEm.getAttribute('id') != 'zzz' , 'Expected getAttributesDict to return copies, but modified original element on "id"'



    def test_setAttributes(self):
        tag = AdvancedTag('div')
        tag.setAttributes( {
            'id' : 'abc',
            'name'  :  'cheese',
            'x-attr' : 'bazing'
        })

        assert tag.getAttribute('id') == 'abc'
        assert tag.getAttribute('name') == 'cheese'
        assert tag.getAttribute('x-attr') == 'bazing'

    def test_specialAttributes(self):
        tag = AdvancedTag('div')
        tag.setAttribute('style', 'position: absolute')
        styleValue = str(tag.getAttribute('style'))
        styleValue = styleValue.strip()
        assert styleValue == 'position: absolute' , 'Expected position: absolute, got %s' %(str(tag.getAttribute('style')),)

        tag.className = 'one two'
        assert str(tag.className).strip() == 'one two' , 'Expected classname to be "one two", got %s' %(repr(str(tag.className).strip()),)

    def test_specialAttributesInHTML(self):
        tag = AdvancedTag('div')
        tag._attributes['style'] = 'position: absolute; color: purple'

        outerHTML = tag.outerHTML

        assert 'position: absolute' in outerHTML , 'Missing style attribute in outerHTML'
        assert 'purple' in outerHTML , 'Missing style attribute in outerHTML'

    def test_classNames(self):
        tag = AdvancedTag('div')
        tag.addClass('abc')

        assert tag.hasClass('abc'), 'Failed to add class'
        assert 'abc' in tag.outerHTML , 'Failed to add class in outerHTML'

        tag.addClass('def')

        assert tag.hasClass('abc'), 'Failed to retain class'
        assert 'abc' in tag.outerHTML , ' Failed to retain in outerHTML'

        assert tag.hasClass('def'), 'Failed to add second class'
        assert 'def' in tag.outerHTML , ' Failed to add to outerHTML'

        tag.removeClass('abc')
        assert not tag.hasClass('abc'), 'Failed to remove class'
        assert 'abc' not in tag.outerHTML , 'Failed to remove class from outerHTML'

        assert tag.hasClass('def'), 'Failed to retain class'
        assert 'def' in tag.outerHTML , ' Failed to retain in outerHTML'


    def test_noValueAttributes(self):
        parser = AdvancedHTMLParser()
        parser.parseStr('<input id="thebox" type="checkbox" checked />')

        tag = parser.getElementById('thebox')
        assert tag.hasAttribute('checked')
        assert 'checked' in tag.outerHTML

    def test_valueMethod(self):
        parser = AdvancedHTMLParser()
        parser.parseStr('<input id="item" type="text" value="hello" />')

        tag = parser.getElementById('item')
        assert tag.value == 'hello'

    def test_attributeDefault(self):
        parser = AdvancedHTMLParser()
        parser.parseStr('<input id="item" type="text" value="hello" />')

        tag = parser.getElementById('item')
        assert tag.getAttribute('type', 'bloogity') == 'text'
        assert tag.getAttribute('woogity', 'snoogity') == 'snoogity'


    def test_setAttributesOnItem(self):
        tag = AdvancedTag('div')

        tag.id = 'hello'


        assert tag.id == 'hello' , 'Expected to be able to set special attribute "id" and have it show up as both attribute and on item'
        assert tag.getAttribute('id', '') == 'hello' , 'Expected to be able to set special attribute "id" and have it show up as both attribute and on item'

        tag.name = 'cheese'

        assert tag.name == 'cheese' , 'Expected to be able to set special attribute "name" and have it show up as both attribute and on item'
        assert tag.getAttribute('name', '') == 'cheese' , 'Expected to be able to set special attribute "name" and have it show up as both attribute and on item'

        assert tag.tabIndex == -1 , 'Expected default tab index (unset) to be -1'

        tag.tabIndex = 5

        assert 'tabindex="5"' in tag.outerHTML , 'Expected setting the tabIndex to set tabindex attribute on html'

    def test_domAttributes(self):

        parser = AdvancedHTMLParser()

        parser.parseStr(''''<html>
        <body>
            <div id="someDiv" class="one two" align="left">
                <span>Some Child</span>
            </div>

        </body>
    </html>
        ''')

        someDivEm = parser.getElementById('someDiv')

        assert someDivEm , 'Failed to get element by id="someDiv"'

        attributes = someDivEm.attributesDOM

        assert attributes['id'].value == 'someDiv' , 'Expected attributes["id"].value to be equal to "someDiv"'

        assert attributes['class'].value == 'one two', "Expected attributes['class'].value to be equal to 'one two'"
        assert attributes['align'].value == 'left' , "Expected attributes['align'].value to be equal to 'left'"

        assert attributes['notset'] is None, 'Expected attributes["notset"] to be None'

        assert attributes['id'].ownerElement == someDivEm , 'Expected ownerElement to be "someDivEm"'

        assert attributes['id'].ownerDocument == parser , 'Expected ownerDocument to be parser'

        assert str(attributes['id']) == 'id="someDiv"' , 'Expected str of attribute to be \'id="someDiv"\' but got: %s' %(str(attributes['id']), )

        attributes['align'].value = 'right'

        assert attributes['align'].value == 'right' , 'Expected to be able to change attribute value by assigning .value. Failed on "align".'

        assert someDivEm.getAttribute('align') == 'right' , 'Expected that changing a property in the attributes map would change the value in parent element'

        attrNames = []
        for attrName in attributes:
            attrNames.append(attrName)

        assert 'id' in attrNames , 'Expected "id" to be returned from iter on attributes'
        assert 'class' in attrNames , 'Expected "class" to be returned from iter on attributes'
        assert 'align' in attrNames , 'Expected "align" to be returned from iter on attributes'

        clonedAttributes = {attrName : attributes[attrName].cloneNode() for attrName in attrNames}

        for attrName in ('id', 'class', 'align'):
            attrValue = clonedAttributes[attrName].value
            origValue = attributes[attrName].value

            assert attrValue == origValue , 'Expected cloned attribute %s to match original, but did not. (clone) %s != %s (orig)' %(attrName, attrValue, origValue)

        assert clonedAttributes['id'].ownerElement is None, 'Expected clone to clear ownerElement'
        assert clonedAttributes['id'].ownerDocument == parser , 'Expected clone to retain same ownerDocument'

        clonedAttributes['align'].value = 'middle'

        assert clonedAttributes['align'].value == 'middle' , 'Expected to be able to change value on cloned attribute'
        assert attributes['align'].value == 'right' , 'Expected change on clone to not affect original'

        assert someDivEm.getAttribute('align') == 'right' , 'Expected change on clone to not affect element'

        assert attributes.getNamedItem('id') == attributes['id'], 'Expected getNamedItem("id") to be the same as attributes["id"]'

    def test_unknownStillAttribute(self):
        '''
            test_unknownStillAttribute - Test that setting an unknwon attribute still sets it in HTML
        '''
        tag = AdvancedTag('div')

        tag.setAttribute('squiggle', 'wiggle')

        htmlStr = str(tag)

        assert 'squiggle="wiggle"' in htmlStr

        squiggleAttrValue = tag.getAttribute('squiggle')

        assert squiggleAttrValue == 'wiggle', "Expected 'squiggle' attribute from tag.getAttribute to return 'wiggle'. Got: " + repr(squiggleAttrValue)


    def test_removeAttribute(self):
        '''
            test_removeAttribute - Test removing attributes
        '''

        tag = AdvancedTag('div')

        tag.setAttribute('align', 'left')
        tag.setAttribute('title', 'Hover text')

        htmlStr = str(tag)

        assert 'align="left"' in htmlStr , 'Expected setAttribute("align", "left") to result in align="left" in HTML representation. Got: ' + htmlStr

        alignAttrValue = tag.getAttribute('align')

        assert alignAttrValue == 'left' , 'Expected getAttribute("align") to return "left" after having set align to "left". Got: ' + repr(alignAttrValue)

        tag.removeAttribute('align')

        htmlStr = str(tag)

        assert 'align="left"' not in htmlStr , 'Expected removeAttribute("align") to remove align="left" from HTML representation. Got: ' + htmlStr

        alignAttrValue = tag.getAttribute('align')

        assert alignAttrValue != 'left' , 'Expected removeAttribute("align") to remove align: left from attributes map. Got: ' + repr(alignAttrValue)


        tag.removeAttribute('title')

        htmlStr = str(tag)

        assert 'align="left"' not in htmlStr , 'Expected after all attributes removed via removeAttribute that align="left" would not be present. Got: ' + htmlStr
        assert 'title=' not in htmlStr , 'Expected after all attributes removed via removeAttribute that align="left" would not be present. Got: ' + htmlStr

        attributes = tag.attributes

        assert 'align' not in attributes , 'Expected to NOT find "align" within the attributes. Got: ' + repr(attributes)
        assert 'title' not in attributes , 'Expected to NOT find "align" within the attributes. Got: ' + repr(attributes)


    def test_delAttributes(self):
        '''
            test_delAttributes - Test deleting attributes
        '''
        tag = AdvancedTag('div')

        tag.setAttribute('id', 'abc')

        tag.style = 'display: block; float: left'

        tagHTML = tag.toHTML()

        assert 'id="abc"' in tagHTML , 'Expected id="abc" to be present in tag html. Got: ' + tagHTML
        assert 'style=' in tagHTML , 'Expected style attribute to be present in tag html. Got: ' + tagHTML

        assert tag.style.display == 'block' , 'Expected style.display to be "block". Style is: ' + str(tag.style)
        assert tag.style.float == 'left' , 'Expected style.float to be "left". Style is: ' + str(tag.style)

        del tag.attributes['id']

        tagHTML = tag.toHTML()

        assert not tag.id , "Expected id to be empty after deleting attribute. It is: " + repr(tag.id)
        assert 'id="abc"' not in tagHTML , 'Expected id attribute to NOT be present in tagHTML after delete. Got: ' + tagHTML

        del tag.attributes['style']

        tagHTML = tag.toHTML()

        assert 'style=' not in tagHTML , 'Expected style attribute to NOT be present in tagHTML after delete. Got: ' + tagHTML
        assert str(tag.style) == '' , 'Expected str(tag.style) to be empty string after delete of style attribute. It was: ' + repr(str(tag.style))
        assert tag.style.display == '' , 'Expected display style property to be cleared after delete of style attribute. Style is: ' + str(tag.style)
        assert tag.style.float == '' , 'Expected float style property to be cleared after delete of style attribute. Style is: ' + str(tag.style)


        tag.style = 'font-weight: bold; float: right'

        tagHTML = tag.toHTML()

        assert 'style=' in tagHTML , 'Expected after deleting style, then setting it again style shows up as HTML attr. Got: ' + tagHTML

        assert 'font-weight: bold' in tagHTML , 'Expected after deleting style, then setting it again the properties show up in the HTML "style" attribute. Got: ' + tagHTML

        assert id(tag.getAttribute('style', '')) == id(tag.style) , 'Expected after deleting style, then setting it again the attribute remains linked.'

        assert tag.style.fontWeight == 'bold' , 'Expected after deleting style, then setting it again everything works as expected. Set style to "font-weight: bold; float: left" but on tag.style it is: ' + str(tag.style)

        tag.addClass('bold-item')
        tag.addClass('blue-font')

        assert 'bold-item' in tag.classList , 'Did addClass("bold-item") but did not find it in classList. classList is: ' + repr(tag.classList)
        assert 'blue-font' in tag.classList , 'Did addClass("blue-font") but did not find it in classList. classList is: ' + repr(tag.classList)

        classes = tag.getAttribute('class')

        assert 'bold-item' in classes and 'blue-font' in classes , 'Expected class attribute to contain both classes. Got: ' + str(classes)

        # This should call del tag._attributes['class']
        tag.removeAttribute('class')

        assert 'bold-item' not in tag.classList , 'After removing class, expected to not find classes in tag.classList. classList is: ' + repr(tag.classList)

        assert len(tag.classList) == 0 , 'Expected to have no classes in classList after delete. Got %d' %(len(tag.classList), )

        assert tag.getAttribute('class') == '' , 'Expected after removing class it would be an empty string'

        assert tag.getAttribute('clazz') is None , 'Expected default getAttribute on non-set attribute to be None'


if __name__ == '__main__':
    sys.exit(subprocess.Popen('GoodTests.py -n1 "%s" %s' %(sys.argv[0], ' '.join(['"%s"' %(arg.replace('"', '\\"'), ) for arg in sys.argv[1:]]) ), shell=True).wait())
