class Tag:
    def __init__(self, tag, toplevel = False, is_single = False, klass = None, text = "", **kwargs):
        self.tag = tag
        self.text = text
        self.toplevel = toplevel
        self.is_single = is_single
        self.children = []
        self.attributes = {}

        if klass is not None:
            self.attributes["class"] = " ".join(klass)
        for attr, value in kwargs.items():
            self.attributes[attr]=value


    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

        if self.children:
            opening = "<{tag}".format(tag=self.tag)
            if attrs:
                opening += " {attrs}".format(attrs=attrs)
            opening += ">\n"
            internal = "%s" % self.text
            for child in self.children:
                internal += (str(child) + "\n")
            ending = "</%s>" % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                opening = "<{tag}".format(tag=self.tag)
                if attrs:
                    opening += " {attrs}".format(attrs=attrs)
                opening += "/>"                
                return opening

            else:
                opening = "<{tag}".format(tag=self.tag)
                if attrs:
                    opening += " {attrs}".format(attrs=attrs)
                opening += ">"
                if self.text:
                    opening += self.text
                else:
                    opening += "\n"
                opening += "</{tag}>".format(tag=self.tag)

                return opening

    # Класс - родитель. Не получилось добавлять пробелы...

class HTML(Tag):
    def __init__(self, output=None):
        self.tag = "html"
        self.toplevel = True
        self.is_single = False
        self.output = output
        self.children = []

    def __exit__(self, type, value, traceback):
        if self.output:
            with open(str(self.output), "w") as f:
                f.write("<%s>/n" % self.tag)
                for child in self.children:
                    f.write(str(child)+"/n")
                f.write("</%s>/n" % self.tag)
        else:
            print("<%s>" % self.tag)
            if self.children:
                for child in self.children:
                    print(child)
            print("</%s>" % self.tag)

    # Добавлен вывод на печать или в файл в зависимости от значения output

class TopLevelTag(Tag):
    def __init__(self, tag, klass="", toplevel=True, **kwargs):
        self.tag = tag
        self.text = ""
        self.toplevel = toplevel
        self.is_single = False
        self.children = []
        self.attributes = {}

        for attr, value in kwargs.items():
            self.attributes[attr]=value

    # Теоретически можно было и без этого...

if __name__ == "__main__":
    with HTML(output=None) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1
 
            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png") as img:
                    div += img

                body += div

            doc += body
