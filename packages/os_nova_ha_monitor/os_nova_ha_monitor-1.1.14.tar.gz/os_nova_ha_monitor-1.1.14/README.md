# Openstack Nova HA monitor package

Openstack Nova HA monitor is monitoring state of ocmpute nodes and when any of them fails it
will initial compute node takeover on HA node.

## Documentation

### Consul K/V store values

_ha_cluster/compute_nodes/{{ compute-node }}/status/failed_
    - fail status of the compute node, if this is set to true, this node is considered failed,
      and will be recovered. If this status becomes "True" it can only be reset to "False"
      manually by Administrator.
_ha_cluster/compute_nodes/{{ compute-node }}/status/recovered_
    - this value is becomes True, once HA node attempts to recover this node. HA nodes only
      try to recover nodes which have "status/failed" set to True and "status/recovered"
      set to "False". Once this becomes True, only andministrator can set it back to False
_ha_cluster/compute_nodes/{{ compute-node }}/internal/number_fails_
    - counter of HA Monitor check interval failures. HA Monitor periodically checks
      health of compute node, and increases this counter. When this counter reaches defined
      threshold, the HA Monitor sets "status/failed" to True.
_ha_cluster/compute_nodes/{{ compute-node }}/internal/runtime_config_
    - runtime local config of the compute node. This config contains all
      required information for performing the recovery.
_ha_cluster/compute_nodes/{{ compute-node }}/config/bmc/user_
    - ilo/ipmi user name used to managed this compute-node remotely
_ha_cluster/compute_nodes/{{ compute-node }}/config/bmc/password_
    - ilo/ipmi user password used to managed this compute-node remotely
_ha_cluster/compute_nodes/{{ compute-node }}/config/bmc/ip_
    - ilo/ipmi ip address used to managed this compute-node remotely
_ha_cluster/compute_nodes/{{ compute-node }}/config/ssh/user_
    - ssh-check required test user login
_ha_cluster/compute_nodes/{{ compute-node }}/config/ssh/password_
    - ssh-check required test user password
_ha_cluster/compute_nodes/{{ compute-node }}/general_
    - empty directory for now

_ha_cluster/ha_nodes/{{ ha-node }}/status/in_use_
    - When HA Node starts recovering a compute node, it marks it sets this value to True,
      to prevent condition where two compute nodes fail at the same time and HA Node tries
      to recover both simultaneously. Updating of this value is in critical section.
_ha_cluster/ha_nodes/{{ ha-node }}/general_
    - empty directory for now

## Development

### Running unit tests

```console
pytest -v -s
```

### Running integration tests

Integration tests are implemented in `tests/integration` directory. They are based on vagrant which will start 2 VMs w


# TODO

1) Split Consul based cluster monitor from NOVA HA recovery part.

2) Create integration tests.