import {Injectable} from '@angular/core'
import {ProductType} from 'app/models/product-type.model'


@Injectable()
export class ProductTypeJsonSerializerService {
    deserialize(productTypeJson: ProductTypeJson): ProductType {
        let productType = {
            pk: productTypeJson.id,
            name: productTypeJson.translations[window.DJANGO.defaultLang]['name'],
        }
        return productType
    }

    deserializeArray(productTypeArrayJson: Array<ProductTypeJson>): Array<ProductType> {
        let productTypeArray = [] as Array<ProductType>
        for (let productTypeJson of productTypeArrayJson) {
            let productType: ProductType = {
                pk: productTypeJson.id,
                name: productTypeJson.translations[window.DJANGO.defaultLang]['name'],
            }
            productTypeArray.push(productType)
        }
        return productTypeArray
    }
}


export interface ProductTypeJson {
    id: PrimaryKey
    identifier: string
    translations: {
        [langCode: string]: {
            [fieldName: string]: string
        }
    }
    attributes: Array<PrimaryKey>
}
