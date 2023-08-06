import os
import git

def clone(url, destination):
    os.makedirs(destination)
    empty_repo = git.Repo.init(destination)
    origin = empty_repo.create_remote('origin', url)
    assert origin.exists()
    assert origin == empty_repo.remotes.origin == empty_repo.remotes['origin']
    origin.fetch()                  # assure we actually have data. fetch() returns useful information
    # Setup a local tracking branch of a remote branch
    empty_repo.create_head('master', origin.refs.master)  # create local branch "master" from remote "master"
    empty_repo.heads.master.set_tracking_branch(origin.refs.master)  # set local "master" to track remote "master
    empty_repo.heads.master.checkout()  # checkout local "master" to working tree
    return True

def update(destination):
    repo = git.Repo(destination)
    origin = repo.remotes.origin
    origin.fetch()
    repo.create_head('master', origin.refs.master, force=True)\
        .set_tracking_branch(origin.refs.master)\
        .checkout()
    repo.head.reset(index=True, working_tree=True)
