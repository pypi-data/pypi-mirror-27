import {Injectable} from '@angular/core'
import {TransStr} from 'app/models/trans-str.model'
import {Type} from 'app/type.enum'
import {Cls} from 'app/models/cls.model'
import {ProductTypeNetworkService} from 'app/services/network/product-type.service'
import {ProductType} from 'app/models/product-type.model'


@Injectable()
export class ClsJsonSerializerService {
    constructor(
        private productTypeService: ProductTypeNetworkService,
    ) { }

    serialize(cls: Cls): ClsJson {
        let clsJson = {
            pk: cls.pk,
            code: cls.code,
            type: cls.type,
            name: cls.name,
            product_type: cls.productType.pk,
        }
        return clsJson
    }

    async deserialize(clsJson: ClsJson): Promise<Cls> {
        let cls: Cls = new Cls({
            pk: clsJson.pk,
            code: clsJson.code,
            type: clsJson.type,
            name: clsJson.name,
            productType: await this.deserializeProductType(clsJson),
            optionsPk: clsJson.options,
            isSaved: true,
        })
        return cls
    }

    private async deserializeProductType(clsJson: ClsJson): Promise<ProductType> {
        let productTypePk = clsJson.product_type
        return await this.productTypeService.get(productTypePk)
    }
}


export interface ClsJson {
    pk?: Optional<PrimaryKey>
    code: string
    type: Type
    name: TransStr
    product_type: PrimaryKey
    options?: Optional<Array<PrimaryKey>>
}
