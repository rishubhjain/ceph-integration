from tendrl.integrations.ceph.objects import osd


class Osd(osd.Osd):
    def __init__(self, id=None,
                 uuid=None, hostname=None, public_addr=None,
                 cluster_addr=None, device_path=None,
                 heartbeat_front_addr=None, heartbeat_back_addr=None,
                 down_at=None, up_from=None, lost_at=None, osd_up=None,
                 osd_in=None, up_thru=None, weight=None,
                 primary_affinity=None, state=None, last_clean_begin=None,
                 last_clean_end=None, total=None, used=None, used_pcnt=None,
                 *args, **kwargs):
        super(Osd, self).__init__(
            id=id,
            uuid=uuid,
            hostname=hostname,
            public_addr=public_addr,
            cluster_addr=cluster_addr,
            device_path=device_path,
            heartbeat_front_addr=heartbeat_front_addr,
            heartbeat_back_addr=heartbeat_back_addr,
            down_at=down_at,
            up_from=up_from,
            lost_at=lost_at,
            osd_up=osd_up,
            osd_in=osd_in,
            up_thru=up_thru,
            weight=weight,
            primary_affinity=primary_affinity,
            state=state,
            last_clean_begin=last_clean_begin,
            last_clean_end=last_clean_end,
            total=total,
            used=used,
            used_pcnt=used_pcnt,
            *args,
            **kwargs
        )
