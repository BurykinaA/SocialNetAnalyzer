"""
This script collects data from VK (VKontakte) social network to analyze your friends network.
It retrieves information about your friends, their connections, and creates a visualization 
of your social network graph. The script collects data such as friends' personal info 
(gender, location, education) and mutual connections between them.
"""

import vk_api
import json
import networkx as nx
import pyvis.network as net


def get_vk_session():
    """Authenticate and create VK session"""
    email = input("Enter your VK email: ")
    password = input("Enter your VK password: ")
    client_secret = input("Enter your VK client_secret: ")

    vk_session = vk_api.VkApi(email, password, app_id=6287487, client_secret=client_secret)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(f"Authentication failed: {error_msg}")
        exit()

    return vk_session.get_api()

def get_friends_list(vk, user_id=None, fields_to_return=['sex', 'country', 'education', 'city', 'bdate']):
    """Collect friends list with their details"""
    raw_list = vk.friends.get(user_id=user_id, fields=fields_to_return)
    friends_list = []

    for friend in raw_list['items']:
        if friend.get('deactivated') != 'deleted':
            friend_new = {}
            sex = 'ж' if friend['sex'] == 1 else 'м'

            bdate = friend.get('bdate', '')
            byear = bdate[-4:] if len(bdate) > 6 else ''

            friend_new.update({
                'name': friend['first_name'] + ' ' + friend['last_name'],
                'name_label': friend['first_name'] + '\n' + friend['last_name'],
                'sex': sex,
                'byear': byear,
                'id': friend['id'],
                'city': friend.get('city', {}).get('title', ''),
                'country': friend.get('country', {}).get('title', ''),
                'faculty_name': friend.get('faculty_name', ''),
                'university_name': friend.get('university_name', '')
            })
            friends_list.append(friend_new)
    
    return friends_list

def save_friends_edges(vk, main_friends_list, name_to_exclude, file_name):
    """Save connections between friends"""
    friends_connections = []
    main_friends_ids = [friend['id'] for friend in main_friends_list]
    list_num_mutfr = []
    main_friends_list_new = []

    for friend in main_friends_list:
        try:
            this_friend_friends = get_friends_list(vk, user_id=friend['id'])
        except Exception as e:
            print(f"Skipping friend {friend['name']} (ID {friend['id']}): {str(e)}")
            continue

        for friend_friend in this_friend_friends:
            edge = tuple(sorted([friend['name'], friend_friend['name']]))
            if (friend_friend['id'] in main_friends_ids and 
                edge not in friends_connections and 
                friend_friend['name'] != name_to_exclude):
                try:
                    mutual_friends = vk.friends.getMutual(
                        source_uid=friend['id'],
                        target_uid=friend_friend['id']
                    )
                except Exception as e:
                    print(f"Skipping mutual friend check for {edge}: {str(e)}")
                    mutual_friends = []
                
                friends_connections.append(edge)
                list_num_mutfr.append(len(mutual_friends))
        
        friend.update({'n_friends': len(this_friend_friends)})
        main_friends_list_new.append(friend)

    with open(f'{file_name}.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join('%s %s' % x for x in friends_connections))

    with open(f'{file_name}_attributes.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join('%s' % x for x in list_num_mutfr))

    return main_friends_list_new

def main():
    vk = get_vk_session()
    
    user_name = input("Enter your first name in VK: ")
    user_lastname = input("Enter your last name in VK: ")
    name_to_exclude = f"{user_name}\n{user_lastname}"

    my_friends_list = get_friends_list(vk)
    with open('friends_list.json', 'w', encoding='utf-8') as f:
        json.dump(my_friends_list, f, ensure_ascii=False, indent=2)

    with open('friends_list.json', 'r', encoding='utf-8') as f:
        my_friends_list = json.load(f)

    my_friends_names = [friend['name'] for friend in my_friends_list]

    my_friends_list = save_friends_edges(vk, my_friends_list, name_to_exclude, 'edges')

    with open('edges.txt', 'r', encoding='utf-8') as f:
        raw_edges = f.readlines()

    with open('edges_attributes.txt', 'r', encoding='utf-8') as f:
        edges_attrs = f.readlines()

    edges = []
    for r_edge in raw_edges:
        line = r_edge.split(' ')
        edge = (line[0] + ' ' + line[1], line[2] + ' ' + line[3].rstrip())
        edges.append(edge)

    edges_attrs = [int(attr) for attr in edges_attrs]

    friends_attributes = dict(zip(my_friends_names, my_friends_list))
    G = nx.Graph()
    G.add_nodes_from(friends_attributes)
    nx.set_node_attributes(G, friends_attributes)
    G.add_edges_from(edges)

    output_path = input("Enter the path to save files (e.g., ./): ")
    nx.write_gexf(G, f"{output_path}/graph.gexf")

    net_vis = net.Network(notebook=True, height="750px", width="100%", cdn_resources='in_line')
    net_vis.from_nx(G)
    net_vis.show(f"{output_path}/network_visualization.html")

if __name__ == "__main__":
    main()