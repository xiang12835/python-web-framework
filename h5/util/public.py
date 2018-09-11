# -*- coding: utf-8 -*-
import logging
from app.index.models import Config
from app.index.lib.util import DateUtil


ALL_CONFIG_OBS = {
    # 0: Element,
    1: Config,
    # 2: PersonalBannerConfig,
    # 3: SoConfig,
    # 4: PopUpConfig,
    # 5: FinishInstallAppProtocolConfig,
    # 6: ToneConfig,
    # 7: LuaConfig,
    # 8: PlayerConfig,
    # 9: PopupPageSwitch,
    # 10: PushHubaoAppConfig,
    # 11: PlayerCommonConfig,
    # 12: VideoActionbarConfig,
}


def get_model_ob_dbs(switch_id, ob, is_update_cache=''):
    config_dbs_x, config_dbs = [], []
    try:
        model_ob = ALL_CONFIG_OBS[ob]
        kwargs = {'is_delete': False, 'state': 1}
        if ob in [0, 12]:
            kwargs['actionbar_id'] = switch_id
            args = {'actionbar_id': switch_id, 'is_delete': False}
        else:
            kwargs['switch_id'] = switch_id
            args = {'switch_id': switch_id, 'is_delete': False}
        config_dbs_x = model_ob.objects.filter(**args).values()
        config_dbs = model_ob.objects.filter(**kwargs).order_by('-position').values()
    except Exception, e:
        logging.error(e)

    return config_dbs_x, config_dbs


def hit_config(switch_id, config_str, model_ob, is_update_cache='', **params):
    today = DateUtil.get_today_int_date()
    result = 0

    try:
        config_dbs_x, config_dbs = get_model_ob_dbs(switch_id=switch_id, ob=model_ob, is_update_cache=is_update_cache)
        if not config_dbs_x:
            return 1

        #没有命中开关时的默认状态
        if not config_dbs:
            result = config_dbs_x[0]['state']
            return result

        configs = config_str.split(',')
        for config_db in config_dbs:
            #print config_db
            hit_map = {}
            start, end = config_db['start'], config_db['end']
            if (today >= start and today <= end) or (start is None and end is None):
                for dim in configs:
                    vals = config_db.get(dim, '')

                    #空值也算命中
                    if not vals:
                        hit_map.update({dim: 1})
                        continue

                    #全部也算命中
                    values = vals.split(',')
                    if 'all' in values:
                        hit_map.update({dim: 1})
                        continue

                    param_val = params.get(dim, '')

                    # print vals 
                    # print param_val
                    # print hit_map

                    if param_val in values:
                        hit_map.update({dim: 1})
                    

                if len(hit_map.keys()) == len(configs):
                    return config_db['state']
                

            
    except Exception, e:
        logging.error(e)

    return 0
