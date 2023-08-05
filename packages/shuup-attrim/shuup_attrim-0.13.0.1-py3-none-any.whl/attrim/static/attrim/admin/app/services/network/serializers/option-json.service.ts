import {TransStr} from 'app/models/trans-str.model'
import {Injectable} from '@angular/core'
import {Option} from 'app/models/option.model'
import {ClsNetworkService} from 'app/services/network/cls.service'


@Injectable()
export class OptionJsonSerializerService {
    constructor(
        private clsService: ClsNetworkService,
    ) { }

    serialize(option: Option): OptionJson {
        if (option.clsPk === null) {
            throw TypeError('Option to serialize must have a class assigned.')
        }
        let optionJson = {
            pk: option.pk,
            cls: option.clsPk,
            value: option.value,
            order: option.order,
        }
        return optionJson
    }

    async deserialize(optionJson: OptionJson): Promise<Option> {
        let option = new Option({
            pk: optionJson.pk,
            clsPk: optionJson.cls,
            type: (await this.clsService.get(optionJson.cls)).type,
            value: optionJson.value,
            order: optionJson.order as Optional<number>,
            isSaved: true,
        })
        return option
    }
}


export interface OptionJson {
    pk?: Optional<PrimaryKey>
    cls: PrimaryKey
    value: number | string | TransStr
    order?: Optional<number>
}
