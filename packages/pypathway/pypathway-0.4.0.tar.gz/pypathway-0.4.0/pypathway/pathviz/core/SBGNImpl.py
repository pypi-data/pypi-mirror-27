import json
import re
import shutil
import time
from xml.dom.minidom import Document
from xml.sax import *
import os
import sys

from ..query.common import PathwayFormat
from ...pathviz.utils import SBGNParseException
from ...pathviz.utils import environment as env
from .BioPAXImpl import NativeBioPAXParser
from .general import Pathway, vertex2id, ReactomeNativeParser


def id_handle(id):
    '''
    In SBGNviz.js if the id contain some spacial characters, will lead to a select failure, so, we replace the
    illegal char in the id

    :param id:
    :return: filtered id
    '''
    if id:
        return "".join([x for x in re.findall(r"[\d\w]{1}", id)]).replace("_", "")
    else:
        return None


# First define the errors:
class TypeNotInNestedElementListError(Exception):
    def __init__(self, input_type, exist_types):
        self.input_type = input_type
        self.exist_types = exist_types


# Bbox not found while visualization
class BboxNotFoundInGlyphException(Exception):
    def __init__(self):
        pass


class ObjectCaller:
    def __init__(self):
        self.dicts = {"notes": [Notes, ["notes"]], "extension": [Extension, ["extension"]],
                      "point": [Point, ["x", "y"]], "bbox": [BBox, ["x", "y", "h", "w"]],
                      "sbgn": [SBGNRoot, ["version"]], "map": [Map, ["language"]],
                      "arc": [Arc, ["class", "id", "source", "target"]], "arcgroup": [ArcGroup, ["class"]],
                      "glyph": [Glyph, ["class", "compartmentOrder", "compartmentRef", "id", "orientation"]],
                      "label": [Label, ["text"]], "state": [State, ["value", "variable"]], "clone": [Clone, ["label"]],
                      "callout": [CallOut, ["target"]],
                      "port": [Port, ["id", "x", "y"]], "start": [Start, ["x", "y"]],
                      "next": [Next, ["x", "y"]], "end": [End, ["x", "y"]]}

    def call(self, name, attrs):
        if name not in self.dicts:
            raise TypeNotInNestedElementListError(name, self.dicts.keys())
        args = [attrs.get(x) for x in self.dicts[name][1]]
        return self.dicts[name][0](*args)


class Heap(list):
    def __init__(self):
        list.__init__([])

    def push(self, element):
        self.insert(0, element)

    def peak(self):
        return self[0]


# A parser for SBGN-PD
class SBGNParser:
    @staticmethod
    def parse(stream, BioPAX=None):
        handler = SBGNHandler()
        parseString(stream, handler)
        if BioPAX:
            handler.root.BioPAX = BioPAX
        return handler.root

    @staticmethod
    def parseFromFile(file, BioPAX=None):
        try:
            if sys.version[0] == "2":
                with open(file) as fp:
                    if BioPAX:
                        with open(BioPAX) as fp2:
                            return SBGNParser.parse(fp.read(), BioPAX=fp2.read())
                    else:
                        return SBGNParser.parse(fp.read(), BioPAX=None)
            else:
                with open(file, encoding="utf8") as fp:
                    if BioPAX:
                        with open(BioPAX, encoding="utf8") as fp2:
                            return SBGNParser.parse(fp.read(), BioPAX=fp2.read())
                    else:
                        return SBGNParser.parse(fp.read(), BioPAX=None)
        except IOError:
            raise SBGNParseException("Fail reading file")
        except Exception as e:
            import traceback
            # print(traceback.format_exc())


# basic class of all SBGN-PD Objects.
class SBGNObject(Pathway):
    def __init__(self, name, ref):
        Pathway.__init__(self)
        self.core_implement = PathwayFormat.SBGN
        self.name = name
        self.ref = ref
        if name == "sbgn":
            self.id = "root"

    def add_child(self, child):
        child.father = self
        if child.name not in self.ref:
            print("Me {}, Child: {} not in {}".format(self.name, child.name, ", ".join(self.ref.keys())))
            raise TypeNotInNestedElementListError(child.name, self.ref.keys())
        try:
            self.ref[child.name].append(child)
        except Exception as e:
            import traceback
            print(self)
            print(traceback.format_exc())
            print(self.name, self.ref)
            exit()

    def summary(self, deepth=0):
        refs = self.ref.values()
        result = []
        for x in refs:
            for y in x:
                result.append(y)
        if not result:
            return "...." * deepth + "class: {}, Props: {}\n".format(self.name, ", ".join(
                ["{}: {}".format(k, v) for k, v in self.__dict__.items()
                 if not k == "name"
                 and not isinstance(v, list)
                 and not isinstance(v, dict)
                 and not k == "father"
                 and not k == "BioPAX"]))
        else:
            result = "...." * deepth + "class: {}, props: {}\n".format(self.name, ", ".join(
                ["{}: {}".format(k, v) for k, v in self.__dict__.items()
                 if not k == "name" and not isinstance(v, list) and not isinstance(v, dict) and not k == "father"
                 and not k == "BioPAX"]))
            for x in refs:
                if x:
                    for y in x:
                        result += y.summary(deepth=deepth + 1)
            return result

    # These properties, is essential in a tree object.
    @property
    def children(self):
        result = []
        for x in self.ref.values():
            for y in x:
                result.append(y)
        return result

    @property
    def root(self):
        father = self.father
        while not isinstance(father, SBGNRoot):
            father = father.father
        return father

    @property
    def is_root(self):
        return isinstance(self, SBGNRoot)

    # this class should not be overwritten
    def export(self):
        raise Exception("You can only use export in a SBGN tree's root")

    def draw(self, setting=None):
        raise NotImplementedError

    # Do not call this method directly, please use root's export method
    def _xml_object(self, father, doc):
        # if hasattr(self, "id") and self.id == "reactionVertex10616398":
        #     print self.bbox
        me = doc.createElement(self.name)
        for k, v in self.__dict__.items():
            if k == "ref" or k == "father" or k == "root" or k == "children" or k == "core_implement" \
                    or k in self.ref.keys() or k == "external_id" or k == "raw_id":
                continue
            if not v and not type(v) == float:
                # if hasattr(self, "name") and self.name == "bbox":
                #     print k, type(v)
                continue
            if k == "type":
                k = "class"
            if sys.version[0] == "2":
                me.setAttribute(k, str(v))
            else:
                if k == "text":
                    me.setAttribute(k, str(v.decode()))
                else:
                    me.setAttribute(k, str(v))
        father.appendChild(me)
        children = self.children
        if self.name == "arc":
            def cmp_s(x, y):
                if x == "start":
                    return -1
                elif x == "next" and y == "end":
                    return -1
                else:
                    return 1
            if sys.version[0] == "2":
                children.sort(cmp=cmp_s, key=lambda x: x.name)
        new = []
        for x in self.children:
            if hasattr(x, "name") and x.name == "bbox":
                new.insert(0, x)
            else:
                new.append(x)
        for x in new:
            x._xml_object(me, doc)

    @property
    def visualize_able(self):
        return False

    @property
    def db_id(self):
        results = []
        if self.ref.get("label"):
            results.append(self.ref.get("label")[0].text)
        return results

    def __repr__(self):
        # return str({k: v for k, v in self.__dict__.items() if not k == "father"
        #             and not k == "children" and not k == "ref"})
        return "class: {}, id: {}, type: {}, external_id: {}".format(self.name,
                                                                     self.id if hasattr(self, "id") else None,
                                                                     self.type if hasattr(self, "type") else None,
                                                                     self.external_id if hasattr(self, "external_id")
                                                                     else None)

    def _flatten(self, list):
        if self.children:
            list.extend([x for x in self.children])
        for x in self.children:
            x._flatten(list)

    def flatten(self):
        result = []
        self._flatten(result)
        return result

    def _structure(self, nodes, edges, elements):
        try:
            for x in self.children:
                nodes.append([x.name, x.id if hasattr(x, "id") else None])
                elements.append({
                    "group": "nodes",
                    "data": {
                        "id": x.id
                    },
                    "css": {
                        "color": "red"
                    }
                })
                edges.append([x.id if hasattr(x, "id") else None, self.id if hasattr(self, "id") else None])
                elements.append({
                    "groups": "edges",
                    "data": {
                        "id": self.id + x.id,
                        "source": x.id,
                        "target": self.id
                    },
                    "css": {
                        "width": "3",
                        "color": "red"
                    }
                })
                x._structure(nodes, edges, elements)
        except:
            print(self)
            exit()

    def structure(self):
        no_id_er = set([x.name for x in self.flatten() if not hasattr(x, "id")])
        for x in no_id_er:
            cx = [t for t in self.flatten() if t.name == x]
            for i, n in enumerate(cx):
                n.id = x + str(i)
        nodes = []
        edges = []
        elements = []
        self._structure(nodes, edges, elements)
        with open("/Users/sheep/WebstormProjects/treeviz/data.json", "w") as fp:
            fp.write(json.dumps(elements))
        return nodes

    @property
    def entities(self):
        exist_entities = ["unspecified entity", "simple chemical", "macromolecule", "nucleic acid feature",
                          "perturing agent", "source sink", "complex"]
        result = []
        for x in self.flatten():
            for e in exist_entities:
                if hasattr(x, "type") and e in x.type:
                    result.append(x)
                    continue
        return result

    @property
    def reactions(self):
        exist_reaction = ["process", "omitted process", "uncertain process", "association", "phenotype", "dissociation"]
        result = []
        for x in self.flatten():
            for e in exist_reaction:
                if hasattr(x, "type") and e in x.type:
                    result.append(x)
                    continue
        return result

    @property
    def nodes(self):
        return self.entities

    @property
    def arcs(self):
        exist_arcs = ["consumption", "production", "modulation", "stimulation", "catalysis", "inhibition", "logic arc",
                      "equivalence arc"]
        result = []
        for x in self.flatten():
            for e in exist_arcs:
                if hasattr(x, "type") and e in x.type:
                    result.append(x)
                    continue
        return result

    @property
    def members(self):
        return self.flatten()

    @property
    def compartments(self):
        result = []
        for x in self.flatten():
            for e in ["compartment"]:
                if hasattr(x, "type") and e in x.type:
                    result.append(x)
                    continue
        return result


# note or notes?
class Notes(SBGNObject):
    def __init__(self, note):
        SBGNObject.__init__(self, "notes", {})
        self.note = note

    @property
    def visualize_able(self):
        return False


class Extension(SBGNObject):
    def __init__(self, extension):
        SBGNObject.__init__(self, "extension", {})
        self.extension = extension

    @property
    def visualize_able(self):
        return False


class Point(SBGNObject):
    def __init__(self, x, y):
        self.extension, self.notes, self.x, self.y = [], [], x, y
        SBGNObject.__init__(self, "point", {"notes": self.notes, "extension": self.extension})

    @property
    def visualize_able(self):
        return False


class BBox(SBGNObject):
    def __init__(self, x, y, h, w):
        self.notes, self.extension = [], []
        SBGNObject.__init__(self, "bbox", {"notes": self.notes, "extension": self.extension})
        self.x, self.y, self.h, self.w = float(x), float(y), float(h), float(w)

    @property
    def visualize_able(self):
        return False


# this is the root class of SBGN
# this class provide the function like a DOM tree
# get_node(entity)_by_id, get_arc_by_id
# defined exception: IDNotFoundINPathwayTree
# When you call SBGNParser.parse(stringbuffer) you get a instance of a pathway.
class SBGNRoot(SBGNObject):
    '''
    The root class of a SBGN-PD graph, the export and draw method are implement here.
    '''

    def __init__(self, version):
        self.father = None
        self.extension, self.notes, self.map, self.version = [], [], [], version
        SBGNObject.__init__(self, "sbgn", {"notes": self.notes, "extension": self.extension, "map": self.map})
        self.BioPAX = None

    @property
    def visualize_able(self):
        return False

    def _get_option(self):
        if self.option:
            content = self.option.json
        else:
            content = {}
        for x in self.entities:
            if x.id not in content:
                if not x.color == "black" or not x.bg_color == "white" or not x.scale == 1 or not x.opacity == 1:
                    content[x.id] = {}
                    content[x.id]['default'] = {
                        "value_changed": {
                            "background-color": x.bg_color,
                            "color": x.color,
                            "opacity": x.opacity,
                            "scale": x.scale
                        }
                    }
            else:
                if 'default' not in content[x.id]:
                    if not x.color == "black" or not x.bg_color == "white" or not x.scale == 1 or not x.opacity == 1:
                        content[x.id]['default'] = {
                            "value_changed": {
                                "background-color": x.bg_color,
                                "color": x.color,
                                "opacity": x.opacity,
                                "scale": x.scale
                            }
                        }
        return content

    def draw(self, setting=None):
        '''
        Export the pathway, options and copy the static dir to the ipython's workdir, run it!
        :param setting: ignore it.
        :return: None
        '''
        area_id = str(time.time()).replace(".", "")
        with open(os.path.dirname(os.path.abspath(__file__)) + "/../static/box.html") as fp:
            con = fp.read()
        content = self._get_option()
        if not os.path.exists(os.getcwd() + "/assets/SBGN/"):
            shutil.copytree(os.path.dirname(os.path.abspath(__file__)) + "/../static/SBGN", os.getcwd() + "/assets/SBGN/")
        with open(os.getcwd() + "/assets/SBGN/sampleapp-components/data/config_{}.json".format(area_id), "w") as fp:
            fp.write(json.dumps(content))
        with open(os.getcwd() + "/assets/SBGN/sampleapp-components/data/pathway_{}.xml".format(area_id), "w") as fp:
            fp.write(self.export())
        con = con.replace("{{path}}", "'assets/SBGN/index_{}.html'".format(area_id))
        con = con.replace("{{ratio}}", "0.7").replace("{{time}}", area_id)
        with open(os.path.dirname(os.path.abspath(__file__)) + "/../static/SBGN/index.html") as fp:
            id_con = fp.read()
        with open(os.getcwd() + "/assets/SBGN/index_{}.html".format(area_id), "w") as fp:
            fp.write(id_con.replace("{{time}}", area_id))
        #js
        with open(os.path.dirname(os.path.abspath(__file__)) + "/../static/SBGN/sampleapp-components/js/interface.js") as fp:
            id_con = fp.read()
        with open(os.getcwd() + "/assets/SBGN/sampleapp-components/js/interface_{}.js".format(area_id), "w") as fp:
            fp.write(id_con.replace("{{time}}", area_id))
        if env():
            # here we are in IPython, import IPython assert here, copy static to target dir
            from IPython.display import HTML
            return HTML(con)
        else:
            import webbrowser
            from ..utils import get_local_http_server
            ls = get_local_http_server(os.getcwd())
            try:
                webbrowser.open_new("http://localhost:{}/assets/SBGN/index_{}.html".format(ls.port, area_id))
            except KeyboardInterrupt:
                exit()

    def share(self, path, toolbox=False, options=None, type='HTML'):
        '''
        This is The function that export plot region with certain settings.

        :param path: the export dir
        :param toolbox: display a toolbox or not
        :param options: the plot setting
        :param type: whether a HTML or a Django template
        :return: export to a target project in the path
        '''
        pass

    def export(self):
        # if format == PathwayFormat.KGML:
        #     Warning("[!] Convert from SBGN-PD to Other format is not supported")
        # elif format == PathwayFormat.SBGN:
        doc = Document()
        root = doc.createElement("sbgn")
        root.setAttribute("xmlns", "http://sbgn.org/libsbgn/pd/0.1")
        for x in self.children:
            x._xml_object(root, doc)
        doc.appendChild(root)
        con = doc.toprettyxml(indent="  ")
        return con

    @property
    def members(self):
        member = []
        for x in self.children:
            member.extend(x.flatten())
        return member

    @property
    def nodes(self):
        '''
        Get the list of visualize node id
        :return: list of id
        '''
        return [x for x in self.members if x.name == "glyph"]

    @property
    def entities(self):
        return self.nodes

    def get_element_by_class(self, class_):
        return [x for x in self.members if x.name == class_]

    def get_element_by_id(self, id):
        return [x for x in self.members if hasattr(x, "id") and x.id == id]

    def get_element_by_type(self, type):
        return [x for x in self.members if hasattr(x, "type") and x.type == type]

    def get_element_by_label(self, name):
        result = []
        for x in self.flatten():
            for c in x.children:
                if c.name == "label":
                    if c.text.decode("utf8") == name:
                        if x not in result:
                            result.append(x)
        return result

    def __getattr__(self, item):
        if item in ["__str__"]:
            raise AttributeError
        if item in ["id", "type", "label", "glyph", "external_id", "name"]:
            return None
        l = self.get_element_by_label(item)
        return l if l else None

    def get_element_by_oid(self, oid):
        result = []
        for x in self.flatten():
            if hasattr(x, "external_id"):
                for d in x.external_id:
                    if oid in d.values():
                        result.append(x)
        return result

    def fix(self):
        '''
        Fix the error while converting to sbgn from BioPAX
        :return: None
        '''
        glyph = {x.id: (float(x.bbox[0].x) + float(x.bbox[0].w) / 2, float(x.bbox[0].y) + float(x.bbox[0].h) / 2.0)
                 for x in self.members if x.name == "glyph" and x.bbox}
        port = {x.id: (x.x, x.y, x.father.id) for x in self.members if x.name == "port"}
        for x in self.members:
            if x.name == "arc":
                if x.source in glyph:
                    x.start[0].x = glyph[x.source][0]
                    x.start[0].y = glyph[x.source][1]
                elif x.source in port:
                    x.start[0].x = port[x.source][0]
                    x.start[0].y = port[x.source][1]
                    x.source = port[x.source][2]
                else:
                    print("Wrong: {}".format(x.source))
                    # raise Exception("Where?")
                if x.target in glyph:
                    x.end[0].x = glyph[x.target][0]
                    x.end[0].y = glyph[x.target][1]
                elif x.target in port:
                    x.end[0].x = port[x.target][0]
                    x.end[0].y = port[x.target][1]
                    x.target = port[x.target][2]
                else:
                    print("Wrong target: {}".format(x.target))
                x.ref["glyph"] = []
        # fix the too large modification
        for x in self.members:
            if x.name == "glyph":
                x.port = []
        for x in self.members:
            if x.name == "state":
                if x.value == "phosres":
                    x.value = "P"
                    r = min(float(x.father.bbox[0].w), float(x.father.bbox[0].h))
                    x.father.bbox[0].w = r
                    x.father.bbox[0].h = r

    def fix_reactome(self, json_data):
        rp = ReactomeNativeParser(json_data)
        pd_delete = []
        simple_refer = {}
        # at last we try to handle state variable
        for x in self.members:
            if not hasattr(x, "id") or not hasattr(x, 'type'):
                continue
            if x.type == 'unit of information' or x.type == 'state variable':
                x.father.ref['glyph'].remove(x)
        for x in self.members:
            if not hasattr(x, "id") or not hasattr(x, 'type'):
                continue
            if x.type == 'simple chemical':
                # print('chemical')
                eid = x.raw_id.split("_")[1]
                bioId = vertex2id(eid)
                # print(bioId)
                json_cor = rp.search_nodes(bioId)
                if not json_cor:
                    # print(x.__dict__)
                    # print("simple chemical, do sth......{}".format(x.ref['label'][0].text))
                    for td in x.father.ref['glyph']:
                        if td.raw_id == x.raw_id:
                            # print(x.raw_id)
                            x.father.ref['glyph'].remove(x)
                            break
                    continue
                else:
                    if bioId not in simple_refer:
                        simple_refer[bioId] = [json_cor, []]
                    simple_refer[bioId][1].append(x)
                #     print("SIMPLE MOLECUALR: {}".format(x.ref['label'][0].text))
                #     if x.ref['label'][0].text.decode('utf8') == 'PI P2':
                #         print('match')
                # x.new_id = json_cor['id']
                # # print(json_cor['connectors'])
                # x.bbox[0].x = json_cor['prop']['x']
                # x.bbox[0].y = json_cor['prop']['y']
                # # x.bbox[0].x = int(float(x.bbox[0].x) / 3)
                # # x.bbox[0].y = int(float(x.bbox[0].y) / 3)
                # x.bbox[0].w = json_cor['prop']['width']
                # x.bbox[0].h = json_cor['prop']['height']
                # if x.ref['label'][0].text.decode('utf8') == 'PI P2':
                #     pass
                    # print('match')
                    # print(json_cor)
                    # print(x.bbox[0].__dict__)
                    # print(x.bbox[0].__dict__)
            elif "entity" in x.id:
                eid = x.raw_id.split("_")[1]
                bioId = vertex2id(eid)
                # print(bioId)
                json_cor = rp.search_node(bioId)
                if not json_cor:
                    # print(x.__dict__)
                    # print("!!!!")
                    for td in x.father.ref['glyph']:
                        if td.raw_id == x.raw_id:
                            print(x.raw_id)
                            x.father.ref['glyph'].remove(x)
                            break
                    continue
                    # raise Exception("!!!!!")
                x.new_id = json_cor['id']
                # print(json_cor['connectors'])
                x.bbox[0].x = json_cor['prop']['x']
                x.bbox[0].y = json_cor['prop']['y']
                x.bbox[0].w = json_cor['prop']['width']
                x.bbox[0].h = json_cor['prop']['height']
                x.label[0].text = json_cor['displayName'].encode('utf8')
                for s in x.children:
                    if s.name == 'glyph':
                        eid = s.raw_id.split("_")[1]
                        bioId = vertex2id(eid)
                        # print(bioId)
                        json_cor = rp.search_node(bioId)
                        if not json_cor:
                            for td in x.father.ref['glyph']:
                                if td.raw_id == x.raw_id:
                                    # print(x.raw_id)
                                    x.father.ref['glyph'].remove(x)
                                    break
                            continue
                        # print(json_cor['prop'])
                        s.bbox[0].x = json_cor['prop']['x'] - 10
                        s.bbox[0].y = json_cor['prop']['y'] - 10
                # make sure what exist in complex
                # try:
                #     cor = pax.find_by_DB_ID(bioId).father
                # except:
                #     raise Exception("cor not found")
                # for n in cor.find_child("xref"):
                #     ref = pax.find_by_id(n.props["rdf:resource"].replace("#", ""))
                #     x.external_id.append({ref.find_child("db")[0].value: ref.find_child("id")[0].value})
                #     # print x.external_id
                #     # step 2: fix the compartments's elements
                #     # print cor.summary()
                #     members = []
                #     if cor.class_ == "bp:Complex":
                #         self._complex_members(cor, members, pax)
                #         fbbox = x.ref["bbox"][0]
                #         # print(members)
                #         # x.ref["glyph"] = []
                #         for i, m in enumerate(members):
                #             if m[1] == "1":
                #                 g = Glyph("macromolecule", None, None, x.id + m[0], None)
                #             else:
                #                 g = Glyph("macromolecule multimer", None, None, x.id + m[0], None)
                #             # print(fbbox.x, fbbox.y, fbbox.w, fbbox.h)
                #             bbox = self.complex_layout(fbbox, i, len(members))
                #             label = Label(m[0])
                #             g.ref["bbox"].append(bbox)
                #             g.ref["label"].append(label)
                #             if m[2]:
                #                 for i, md in enumerate(m[2]):
                #                     sg = Glyph("state variable", None, None, x.id + m[0] + md, None)
                #                     sg.ref["bbox"].append(BBox(bbox.x - 6 + (i % 2) * bbox.w,
                #                                                bbox.y - 6 + (i / 2) * bbox.h, 12, 12))
                #                     if "phospho" in md:
                #                         md = "P"
                #                     sg.ref["state"].append(State(value=md, variable=None))
                #                     g.ref["glyph"].append(sg)
                #             x.ref["glyph"].append(g)
                            # print x.summary()
            elif x.type == 'process':
                if x.bbox[0].x == 0 and x.bbox[0].y == 0:
                    pd_delete.append(x.id)
                # print(x.bbox[0].__dict__)
                eid = x.raw_id.split("_")[1]
                bioId = vertex2id(eid)
                # print('pbioid: {}'.format(bioId))
                json_cor = rp.search_edge(bioId)
                if not json_cor:
                    for td in x.father.ref['glyph']:
                        if td.raw_id == x.raw_id:
                            # print(x.raw_id)
                            x.father.ref['glyph'].remove(x)
                            break
                    # print('!!!!!!')
                    continue
                x.new_id = json_cor['id']
                # print(json_cor.get('reactionType'))
                # print(x.type)
                x.type = (json_cor.get('reactionType') or x.type).lower()
                # print(x.type, x.type.lower())
                # if x.type == 'Association':
                #     x.type = 'association'
                # if x.type == 'Omitted Process':
                #     x.type = 'omitted process'
                # for s in json_cor.get['segments']:
                #     if s['segments']:
                #         print(x)
                #         self.arcs.append(Arc(x['type'], s['edgeId'], ))
                # deltax = float(json_cor['position']['x']) - float(x.bbox[0].x)
                # deltay = float(json_cor['position']['y']) - float(x.bbox[0].y)
                x.bbox[0].x = json_cor['position']['x']
                x.bbox[0].y = json_cor['position']['y']
                # print(x.bbox[0].__dict__)
                # print('process: {}, {}, {}'.format(x.id, x.bbox[0].x, x.bbox[0].y))
                x.bbox[0].w = 16
                x.bbox[0].h = 16
                x.ref['port'] = []
        # delete exist compartments
        back = []
        # print(1)
        # print(simple_refer[179856][1])
        # print(1)
        for k, v in simple_refer.items():
            # print("start {}".format(k))
            for sb in v[1]:
                # print(sb)
                tgt = None
                for x in self.members:
                    if hasattr(x, 'name'):
                        if x.name == 'arc':
                            if x.source == sb.id:
                                # print("fetch!: {} to {}".format(sb.id, x.target))
                                tgt = x.target
                                break
                            elif x.target == sb.id:
                                tgt = x.source
                                # print('fetch!: {} to {}'.format(sb.id, x.source))
                                break
                if not tgt:
                    raise Exception("No cor edge found")
                cor = None
                for x in self.members:
                    if hasattr(x, 'id'):
                        if x.id == tgt:
                            bioId = vertex2id(x.raw_id.split('_')[1])
                            cor = rp.search_edge(bioId)
                            # print('Found node', x.raw_id, bioId)
                            # print(cor)
                if not cor:
                    sb.father.ref['glyph'].remove(sb)
                    continue
                cor_data = None
                for k, crv in cor.items():
                    if k in ['inputs', 'catalysts', 'outputs']:
                        for ee in crv:
                            for eesb in v[0]:
                                # print(ee['id'], eesb['id'])
                                if ee['id'] == eesb['id']:
                                    # print("EESAMA is sb: {}".format(ee['id']))
                                    cor_data = eesb

                if not cor_data:
                    pass
                    # print("Failed to find cor simple chemical")
                # print(cor_data)
                # set the prop
                sb.bbox[0].x = cor_data['prop']['x']
                sb.bbox[0].y = cor_data['prop']['y']
                sb.bbox[0].w = cor_data['prop']['width']
                sb.bbox[0].h = cor_data['prop']['height']
        for x in self.members:
            # print(x)
            if hasattr(x, "type") and x.type == "compartment":
                back.append(x)
                x.father.ref['glyph'].remove(x)
            if hasattr(x, "type") and x.type == 'complex':
                # print("we fatch a complex")
                x.type = 'macromolecule'
            # else:
            #     print(x.type)
        # add new compartments:
        for i, x in enumerate(rp.data['compartments']):
            c = back[i]
            c.id = 'compartment{}'.format(x['reactomeId'])
            c.ref['label'][0].text = x['displayName'].encode('utf8')
            bb = c.bbox[0]
            bb.x, bb.y, bb.w, bb.h = x['prop']['x'], x['prop']['y'], x['prop']['width'], x['prop']['height']
            self.map[0].ref['glyph'].append(c)
            if not x.get('componentIds'):
                break
            for cm in x['componentIds']:
                # print(cm)
                for m in self.members:
                    if hasattr(m, 'new_id'):
                        if m.new_id == int(cm):
                            # print("!!!")
                            # print(m)
                            m.compartmentRef = c.id

    def fix_reactome2(self, ratio=2.2):
        '''
        Special for reactome source pathway, need BioPAX data, and json_data
        1. repair complex
        2. repair scale
        3. repair the external ID
        :param ratio:
        :return:
        '''
        # first delete the arcs, let us try nodes
        # self.children[0].ref["arc"] = []
        print('fix reactome')
        for x in self.members:
            if x.name == "port":
                # print x.father.bbox[0].x, x.father.bbox[0].y, x.x, x.y
                x.x = float(x.father.bbox[0].x) / ratio + float(x.x) - float(x.father.bbox[0].x)
                x.y = float(x.father.bbox[0].y) / ratio + float(x.y) - float(x.father.bbox[0].y)
        for x in self.members:
            if x.name == "glyph":
                if x.type == "compartment":
                    if x.bbox:
                        print("w: {}, h: {}, x: {}, y: {}".format(x.bbox[0].w, x.bbox[0].h, x.bbox[0].x, x.bbox[0].y))
                        x.bbox[0].w = (float(x.bbox[0].w) + float(x.bbox[0].x)) / ratio - float(x.bbox[0].x) / ratio
                        x.bbox[0].h = (float(x.bbox[0].h) + float(x.bbox[0].y)) / ratio - float(x.bbox[0].y) / ratio
                        x.bbox[0].x = float(x.bbox[0].x) / ratio
                        x.bbox[0].y = float(x.bbox[0].y) / ratio
                        print("w: {}, h: {}, x: {}, y: {}".format(x.bbox[0].w, x.bbox[0].h, x.bbox[0].x, x.bbox[0].y))
                else:
                    if x.bbox:
                        x.bbox[0].x = float(x.bbox[0].x) / ratio
                        x.bbox[0].y = float(x.bbox[0].y) / ratio
        # for x in self.members:
        #     if hasattr(x, "id") and x.id == "reactionVertex10616398":
        #         print x
        # filter compartments
        print('fix compartments')
        for x in self.members:
            if hasattr(x, "type") and x.type == "compartment":
                print("C before: {}".format(x.raw_id))
        refs = []
        for x in self.members:
            if hasattr(x, "type") and x.type == "compartment":
                refs.append([x, [x.bbox[0].x, x.bbox[0].y, float(x.bbox[0].w) + float(x.bbox[0].x),
                                 float(x.bbox[0].h) + float(x.bbox[0].y)], []])
        for x in self.members:
            if x.name == "bbox" and hasattr(x.father, "type") and x.father.type != "compartment":
                bd = [(float(x.x), float(x.y)),
                      (float(x.x), float(x.h) + float(x.y)),
                      (float(x.w) + float(x.x), float(x.y)),
                      (float(x.w) + float(x.x), float(x.h) + float(x.y))]
                for r in refs:
                    for p in bd:
                        if self._check_point(p, r[1]):
                            state = True
                            r[2].append(x.father.id)

        for x in refs:
            print(x)
        need_delete = [r[0].id for r in refs if len(r[2]) == 0]
        print(need_delete)
        # for x in refs:
        #     print x[0].id, len(x[2])
        temp = []
        for x in self.children[0].glyph:
            if x.id not in need_delete:
                temp.append(x)
        self.children[0].ref["glyph"] = temp
        for x in self.members:
            if hasattr(x, "type") and x.type == "compartment":
                print("C after: {}".format(x.raw_id))
                print(x.father)
        # fix complex and id_ref
        # parse first:
        pax = NativeBioPAXParser.parse(self.BioPAX)
        # we now have a json, lol
        with open('/Users/yangxu/Desktop/investage/R-HSA-1266695.json') as fp:
            graph = json.load(fp)
        rp = ReactomeNativeParser(graph)
        print("prepare to fix biopax")
        # self.children[0].ref['arc'] = []
        # print(self.map[0].children)
        pd_delete = []
        for x in self.members:
            if not hasattr(x, "id") or not hasattr(x, 'type'):
                continue
            # print(x.type, x)
            if "compartment" in x.id:
                print("C: {}".format(x.raw_id))
                print(x.__dict__)
                # ignore now
                cid = x.raw_id.split("_")[2]
                # print(cid, vertex2id(cid))
            elif x.type == 'unit of information' or x.type == 'state variable':
                # print(x.bbox[0].__dict__)
                # print(x.ref['label'][0].text)
                eid = x.raw_id.split("_")[1]
                bioId = vertex2id(eid)
                # print(bioId)
                json_cor = rp.search_node(bioId)
                # print(json_cor['prop'])
                x.bbox[0].x = json_cor['prop']['x']
                x.bbox[0].y = json_cor['prop']['y']
                x.bbox[0].w = json_cor['prop']['width']
                x.bbox[0].h = json_cor['prop']['height']
            elif x.type == 'process':
                if x.bbox[0].x == 0 and x.bbox[0].y == 0:
                    pd_delete.append(x.id)
                # print(x.bbox[0].__dict__)
                eid = x.raw_id.split("_")[1]
                bioId = vertex2id(eid)
                # print('pbioid: {}'.format(bioId))
                json_cor = rp.search_edge(bioId)
                # print(json_cor['segments'])
                # for s in json_cor.get['segments']:
                #     if s['segments']:
                #         print(x)
                #         self.arcs.append(Arc(x['type'], s['edgeId'], ))
                deltax = float(json_cor['position']['x']) - float(x.bbox[0].x)
                deltay = float(json_cor['position']['y']) - float(x.bbox[0].y)
                x.bbox[0].x = json_cor['position']['x']
                x.bbox[0].y = json_cor['position']['y']
                # print(x.bbox[0].__dict__)
                # print('process: {}, {}, {}'.format(x.id, x.bbox[0].x, x.bbox[0].y))
                x.bbox[0].w = 10
                x.bbox[0].h = 10
                x.ref['port'] = []

                # for px in x.children:
                #     if px.name == 'port':
                #         print(px.__dict__)
                #         px.x += deltax
                #         px.y += deltay
                # x.bbox[0].width = json_cor['position']['width']
                # x.bbox[0].height = json_cor['position']['height']

            elif "entity" in x.id:
                eid = x.raw_id.split("_")[1]
                bioId = vertex2id(eid)
                # print(bioId)
                json_cor = rp.search_node(bioId)
                # print(json_cor['connectors'])
                x.bbox[0].x = json_cor['prop']['x']
                x.bbox[0].y = json_cor['prop']['y']
                # x.bbox[0].w = json_cor['prop']['width']
                # x.bbox[0].h = json_cor['prop']['height']
                for s in x.children:
                    if s.name == 'glyph':
                        eid = s.raw_id.split("_")[1]
                        bioId = vertex2id(eid)
                        # print(bioId)
                        json_cor = rp.search_node(bioId)
                        # print(json_cor['prop'])
                        s.bbox[0].x = json_cor['prop']['x'] - 10
                        s.bbox[0].y = json_cor['prop']['y'] - 10
                        # print(x.type)
                        # s.bbox[0].w = json_cor['prop']['width']
                        # s.bbox[0].h = json_cor['prop']['height']

                        # if not bioId:
                #     # print("None corID")
                #     raise SBGNParseException("No corID find")
                # else:
                #     try:
                #         cor = pax.find_by_DB_ID(bioId).father
                #     except:
                #         # print(eid, bioId)
                #         continue
                #     for n in cor.find_child("xref"):
                #         ref = pax.find_by_id(n.props["rdf:resource"].replace("#", ""))
                #         x.external_id.append({ref.find_child("db")[0].value: ref.find_child("id")[0].value})
                #     # print x.external_id
                #     # step 2: fix the compartments's elements
                #     # print cor.summary()
                #     members = []
                #     if cor.class_ == "bp:Complex":
                #         self._complex_members(cor, members, pax)
                #         fbbox = x.ref["bbox"][0]
                #         # print members
                #         # x.ref["glyph"] = []
                #         for i, m in enumerate(members):
                #             if m[1] == "1":
                #                 g = Glyph("macromolecule", None, None, x.id + m[0], None)
                #             else:
                #                 g = Glyph("macromolecule multimer", None, None, x.id + m[0], None)
                #             bbox = self.complex_layout(fbbox, i)
                #             label = Label(m[0])
                #             g.ref["bbox"].append(bbox)
                #             g.ref["label"].append(label)
                #             if m[2]:
                #                 for i, md in enumerate(m[2]):
                #                     sg = Glyph("state variable", None, None, x.id + m[0] + md, None)
                #                     sg.ref["bbox"].append(BBox(bbox.x - 11 + (i % 2) * bbox.w,
                #                                                bbox.y - 11 + (i / 2) * bbox.h, 22, 22))
                #                     if "phospho" in md:
                #                         md = "P"
                #                     sg.ref["state"].append(State(value=md, variable=None))
                #                     g.ref["glyph"].append(sg)
                #             x.ref["glyph"].append(g)
                #             # print x.summary()

        for x in self.members:
            # print(x)
            if not hasattr(x, "id") or not hasattr(x, 'type'):
                continue
            if "edge" in x.id:
                # ignore now
                # print(x.id, x.source, x.target)
                src = self.get_element_by_id(x.source)[0].bbox[0]
                tgt = self.get_element_by_id(x.target)[0].bbox[0]
                # print(src.x, src.y)
                # print(tgt.x, tgt.y)
                x.start[0].x = src.x
                x.start[0].y = src.y
                x.end[0].x = tgt.x
                x.end[0].y = tgt.y
                # print(x.start[0].x, x.start[0].y)
                # print(x.end[0].x, x.end[0].y)
                # rid = x.id.replace('edge', '')
                # bioId = vertex2id(rid)
                # print(rid, bioId)
                # print('rt: {}'.format(bioId))

    def complex_layout(self, bbox, i, total):
        # print('layout: {}, {}, {}'.format(bbox, i, total))
        min_height = 16
        min_width = 36
        if total == 1:
            return bbox
        elif total == 2:
            # h = bbox.h / 2 - 2 if bbox.h / 2 - 2 > min_height else min_height
            h = min_height
            if i == 0:
                return BBox(bbox.x, bbox.y, h, bbox.w)
            else:
                return BBox(bbox.x, bbox.y + h + 2, h, bbox.w)
        elif total == 3:
            # h = bbox.h / 3 - 2 if bbox.h / 3 - 2 > min_height else min_height
            h = min_height
            if i == 0:
                return BBox(bbox.x, bbox.y, h, bbox.w)
            elif i == 1:
                return BBox(bbox.x, bbox.y + h + 2, h, bbox.w)
            else:
                return BBox(bbox.x, bbox.y + 2 * (h + 2), h, bbox.w)
        elif total == 4:
            # h = bbox.h / 2 - 2 if bbox.h / 2 - 2 > min_height else min_height
            # w = bbox.w / 2 - 2 if bbox.w / 2 - 2 > min_width else min_width
            h, w = min_height, min_width
            if i % 2 == 0:
                return BBox(bbox.x, bbox.y + h * (i / 2) + 2, h, w)
            else:
                return BBox(bbox.x + w + 2, bbox.y, h, w)

        elif total > 4:
            # h = bbox.h / math.ceil(total / 3.0) if bbox.h / math.ceil(total / 3.0) > min_height else min_height
            # w = bbox.w / 3 if bbox.w / 3 > min_width else min_width
            h, w = min_height, min_width
            if i % 3 == 0:
                return BBox(bbox.x, bbox.y + (i / 3) * (h + 2), h, w)
            elif i % 3 == 1:
                return BBox(bbox.x + w + 2, bbox.y + (i - 1) / 3 * (h + 2), h, w)
            elif i % 3 == 2:
                return BBox(bbox.x + 2 * w + 4, bbox.y + (i - 2) / 3 * (h + 2), h, w)


    def _complex_members(self, pax, result, root, s=None):
        # for x in pax.find_child("componentStoichiometry"):
        #     print root.find_by_id(x.props["rdf:resource"].replace("#", "")).summary()
        cs = pax.find_child("componentStoichiometry")
        cp = pax.find_child("component")
        if not len(cs) == len(cp):
            raise SBGNParseException("count of componentStoichiometry != count of component")
        info = []
        for x in range(len(cs)):
            info.append((cs[x], cp[x]))
        if pax.class_ == "bp:Complex":
            for s, p in info:
                # print x.props["rdf:resource"].replace("#", "")
                target = root.find_by_id(p.props["rdf:resource"].replace("#", ""))
                if target:
                    self._complex_members(target, result, root, s)
        else:
            # print pax.summary()
            display = pax.find_child("displayName")
            if display:
                # may be unstable
                mods = []
                count = 1
                for x in pax.find_child("feature"):
                    if root.find_by_id(x.props["rdf:resource"].replace("#", "")).class_ == "bp:ModificationFeature":
                        target = \
                        root.find_by_id(x.props["rdf:resource"].replace("#", "")).find_child("modificationType")[0]
                        modf = root.find_by_id(target.props["rdf:resource"].replace("#", ""))
                        if modf:
                            if modf.find_child("term"):
                                mods.append(modf.find_child("term")[0].value)
                if s:
                    if root.find_by_id(s.props["rdf:resource"].replace("#", "")):
                        if root.find_by_id(s.props["rdf:resource"].replace("#", "")).find_child(
                                "stoichiometricCoefficient"):
                            count = root.find_by_id(s.props["rdf:resource"].replace("#", "")).find_child(
                                "stoichiometricCoefficient")[0].value
                result.append([display[0].value, count, mods])

    def _check_point(self, p, bbox):
        if bbox[0] < p[0] < bbox[2] and bbox[1] < p[1] < bbox[3]:
            return True
        else:
            return False


class Map(SBGNObject):
    def __init__(self, language):
        self.arc, self.arcgroup, self.bbox, self.extension, self.glyph, self.notes = [], [], [], [], [], []
        SBGNObject.__init__(self, "map", {"arc": self.arc, "arcgroup": self.arcgroup, "bbox": self.bbox,
                                          "extension": self.extension, "glyph": self.glyph, "notes": self.notes})
        self.language = language

    @property
    def visualize_able(self):
        return False


# this is a PD implement so no port currently
class Arc(SBGNObject):
    def __init__(self, type, id, source, target):
        self.end, self.extension, self.glyph, self.next_element, self.notes, self.start = [], [], [], [], [], []
        SBGNObject.__init__(self, "arc", {"end": self.end, "extension": self.extension, "glyph": self.glyph,
                                          "next": self.next_element, "notes": self.notes, "start": self.start})

        self.type = type
        self.id = id_handle(id)
        self.source = id_handle(source)
        self.target = id_handle(target)

    @property
    def visualize_able(self):
        return True


class ArcGroup(SBGNObject):
    def __init__(self, type):
        self.arc, self.extension, self.glyph, self.note, type = [], [], [], [], type
        SBGNObject.__init__(self, "arcgroup", {"arc": self.arc, "extension": self.extension, "glyph": self.glyph,
                                               "note": self.note})

    # note that arcgroup itself cannot be visualized
    # but its child could
    @property
    def visualize_able(self):
        return False


# entity only used in AF, ignore
class Glyph(SBGNObject):
    def __init__(self, type, compartmentOrder, compartmentRef, id, orientation):
        self.notes, self.extension, self.label, self.state, self.clone, self.callout = [], [], [], [], [], []
        self.bbox, self.glyph, self.port, self.point = [], [], [], []
        SBGNObject.__init__(self, "glyph", {"notes": self.notes, "extension": self.extension, "label": self.label,
                                            "state": self.state, "clone": self.clone, "callout": self.callout,
                                            "bbox": self.bbox, "glyph": self.glyph, "port": self.port,
                                            "point": self.point})
        self.type, self.compartmentOrder = type, compartmentOrder
        self.compartmentRef, self.orientation = compartmentRef, orientation
        self.id = id_handle(id)
        self.raw_id = id
        self.external_id = []
        # default value for display.
        self.color = "black"
        self.bg_color = "white"
        self.opacity = 1
        self.scale = 1

    @property
    def visualize_able(self):
        return True


class Label(SBGNObject):
    def __init__(self, text):
        self.notes, self.extension, self.bbox = [], [], []
        SBGNObject.__init__(self, "label", {"notes": self.notes, "extension": self.extension, "bbox": self.bbox})
        self.text = text.encode("utf8")

    @property
    def visualize_able(self):
        return True


class State(SBGNObject):
    def __init__(self, value, variable):
        self.value = value
        self.variable = variable
        SBGNObject.__init__(self, "state", {})

    @property
    def visualize_able(self):
        return True


class Clone(SBGNObject):
    def __init__(self, label=None):
        self.label = label
        SBGNObject.__init__(self, "clone", {})

    @property
    def visualize_able(self):
        return True


class CallOut(SBGNObject):
    def __init__(self, target):
        self.point, self.target = [], target
        SBGNObject.__init__(self, "callout", {"point": self.point})

    # is it?
    @property
    def visualize_able(self):
        return False


class Port(SBGNObject):
    def __init__(self, id, x, y):
        self.notes, self.extension, self.x, self.y, self.id = [], [], x, y, id_handle(id)
        SBGNObject.__init__(self, "port", {"notes": self.notes, "extension": self.extension})

    @property
    def visualize_able(self):
        return False


class Start(SBGNObject):
    def __init__(self, x, y):
        self.x, self.y = float(x), float(y)
        SBGNObject.__init__(self, "start", {})

    @property
    def visualize_able(self):
        return False


class Next(SBGNObject):
    def __init__(self, x, y):
        self.x, self.y, self.point = float(x), float(y), []
        SBGNObject.__init__(self, "next", {"point": self.point})

    @property
    def visualize_able(self):
        return False


class End(SBGNObject):
    def __init__(self, x, y):
        self.x, self.y, self.point = float(x), float(y), []
        SBGNObject.__init__(self, "end", {"point": self.point})

    @property
    def visualize_able(self):
        return False


# A Handler class
class SBGNHandler(ContentHandler):
    def __init__(self):
        ContentHandler.__init__(self)
        self.root = SBGNRoot("")
        self.heap = Heap()
        self.caller = ObjectCaller()

    def startElement(self, name, attrs):
        if name == "sbgn":
            self.root.name = "sbgn"
            self.root.attrs = attrs
            self.heap.push(self.root)
            return
        if "sbgn" in name:
            name = name.replace("sbgn:", "")
        super_name = self.heap.peak()
        current = self.caller.call(name, attrs)
        super_name.add_child(current)
        self.heap.push(current)

    def endElement(self, name):
        if not name == "sbgn" and "sbgn" in name:
            name = name.replace("sbgn:", "")
        if self.heap.peak().name != name:
            print("should be: {} and is {}".format(name, self.heap.peak().name))
            raise AttributeError
        self.heap.pop(0)
