from gitlab import GraphQLGitlab


def test_graphql_query_current_user(graphql_gl: GraphQLGitlab):
    query = """
query {
  currentUser {
    username
  }
}
"""
    graphql_gl.enable_debug()
    result = graphql_gl.execute(query)
    assert result["user"]["username"] == "root"
