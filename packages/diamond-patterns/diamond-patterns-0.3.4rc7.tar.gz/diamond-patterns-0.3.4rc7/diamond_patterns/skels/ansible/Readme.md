# ansible

This pattern provides for the management of a cloud of Linux machines.
It is simple enough to manage a single machine, but ansible is capable of easily scaling up to support lots of similar machines.

## bootstrapping

Ansible requires python on both the local host and the remote host.
In addition, the `ansible` python packages need to be installed on both sides.
Lastly, a designated user must be created for remote administration of the host via ssh.

    make depends
    make bootstrap
    make ping

If the ping succeeds - i.e. it replies with a pong - then the system is now ready to be controlled with ansible.

## usage

Ansible uses 3 key files to manage hosts:

- **inventory**: which hosts are managed
- **playbook.yaml**: which roles are applied to which hosts
- **/roles**: specific instructions for the roles

To create a role, create a new directory in `/roles` with the name for the role.
Then, create a subdirectory within the newly created folder called `tasks`.
Within that folder, create `main.yaml` to contain task instructions.

Most of the action happens in `/roles/WHATEVER/tasks/main.yaml`.

A simple task looks like:

    ---
    - name: Create the 'testing' user
      user: name=testing shell=/bin/zsh

To perform a dry-run of the changes:

    make dry-run

Finally, to apply the changes to the host:

    make install
