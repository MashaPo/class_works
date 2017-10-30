import re
from subprocess import call
import os
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
#G = nx.read_gexf('graph.gexf')
VAL_POS = ["A", "S", "V", "ADV"]

def wordlist(file):
    wordlist = []
    with open(file, 'r', encoding='utf-8') as source:
        for line in source:
            if '??' not in line:  # пропускаем неизвестные
                lemma, pos = re.split('[{,=]', line)[1:3]
                if pos in VAL_POS:
                    wordlist.append(lemma)
        return wordlist

def graph_append(wordlist):
    G.add_nodes_from(wordlist) #добавляются только новые слова
    for i,l in enumerate(wordlist):
        if i == len(wordlist)-3:
            G.add_edges_from([(l,wordlist[i+1]),(l,wordlist[i+2]),(wordlist[i+1],wordlist[i+2])])
            break
        else:
            G.add_edges_from([(l,wordlist[i+1]),(l,wordlist[i+2]),(l,wordlist[i+3])])

def graph_about():
    print('number of nodes {}'.format(nx.number_of_nodes(G)))
    print('number of edges {}'.format(nx.number_of_edges(G)))
    print('radius {}'.format(nx.radius(G)))
    print('diameter {}'.format(nx.diameter(G)))
    print('average_clustering {}'.format(nx.average_clustering(G)))
    print('transitivity {}'.format(nx.transitivity(G)))
    print('density {}'.format(nx.density(G)))
    print('degree_pearson_correlation_coefficient {}'.format(nx.degree_pearson_correlation_coefficient(G)))
    deg = nx.degree_centrality(G)
    nodes = []
    for node in sorted(deg, key=deg.get, reverse=True):
        nodes.append(node)
    #print('top central nodes: {}'.format(' '.join(nodes[:20])))
    sub_G = G.subgraph(nodes[:30])#визуализируем центральные узлы и их связи
    visualize(sub_G,'graph_top30.png')
    visualize(G,'graph_total.png')

def visualize(g,name):
    pos = nx.random_layout(g)
    nx.draw_networkx_nodes(g, pos, node_color='grey', node_size=2)
    nx.draw_networkx_edges(g, pos, edge_color='green')
    nx.draw_networkx_labels(g, pos, font_size=8, font_family='Arial')
    plt.axis('off')
    plt.savefig(name)
    #plt.show()


def main():
    #разбираем все тексты в corpus, создается morph_corpus
    files = os.listdir('corpus')
    #print(files)
    new_dir = 'morph_corpus/'
    for file in files:
        input_file = 'corpus/' + file
        output_file = new_dir + file
        mystem_call = 'mystem.exe -idn {} {}'.format(input_file, output_file)
        call(mystem_call)
        wlist = wordlist(output_file)
        graph_append(wlist)
    nx.write_gexf(G, 'graph.gexf')
    graph_about()

if __name__ == '__main__':
        main()

