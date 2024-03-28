release_name = "Demo Release"
release_tag_name = "v1.2.3"
release_description = "release notes go here"

link_data = {"url": "https://example.com", "name": "link_name"}


def test_create_project_release(project, project_file):
    project.refresh()  # Gets us the current default branch
    release = project.releases.create(
        {
            "name": release_name,
            "tag_name": release_tag_name,
            "description": release_description,
            "ref": project.default_branch,
        }
    )

    assert release in project.releases.list()
    assert project.releases.get(release_tag_name)
    assert release.name == release_name
    assert release.tag_name == release_tag_name
    assert release.description == release_description


def test_create_project_release_no_name(project, project_file):
    unnamed_release_tag_name = "v2.3.4"

    project.refresh()  # Gets us the current default branch
    release = project.releases.create(
        {
            "tag_name": unnamed_release_tag_name,
            "description": release_description,
            "ref": project.default_branch,
        }
    )

    assert release in project.releases.list()
    assert project.releases.get(unnamed_release_tag_name)
    assert release.tag_name == unnamed_release_tag_name
    assert release.description == release_description


def test_update_save_project_release(project, release):
    updated_description = f"{release.description} updated"
    release.description = updated_description
    release.save()

    release = project.releases.get(release.tag_name)
    assert release.description == updated_description


def test_delete_project_release(project, release):
    project.releases.delete(release.tag_name)


def test_create_project_release_links(project, release):
    release.links.create(link_data)

    release = project.releases.get(release.tag_name)
    assert release.assets["links"][0]["url"] == link_data["url"]
    assert release.assets["links"][0]["name"] == link_data["name"]
