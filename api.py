from flask import Flask, request, abort, jsonify, url_for
from flask_cors import CORS

from controller.group_controller import GroupController
from controller.match_controller import MatchController
from init_config import InitConfig
from controller import PlayerController, TeamController, ChampionshipController

app = Flask(__name__)
CORS(app)


def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, view_func=view_func, methods=['POST', 'PUT', 'OPTIONS', 'PATCH'])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func, methods=['GET', 'PUT', 'DELETE'])
    app.add_url_rule('%s/list' % url, view_func=view_func, methods=['GET'])


register_api(PlayerController, 'player_api', '/player/', pk='id')
register_api(TeamController, 'team_api', '/team/', pk='id')
register_api(ChampionshipController, 'championship_api', '/championship/', pk='id')
register_api(GroupController, 'group_api', '/groups/', pk='id')
register_api(MatchController, 'match_api', '/match/', pk='id')

if __name__ == "__main__":
    config = InitConfig().get_config()
    app.run(host='0.0.0.0', port=config["port"], debug=True)
