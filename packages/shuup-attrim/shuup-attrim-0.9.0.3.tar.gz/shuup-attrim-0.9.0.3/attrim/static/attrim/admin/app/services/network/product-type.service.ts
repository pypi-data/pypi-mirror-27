import {Injectable} from '@angular/core'
import {ProductType} from 'app/models/product-type.model'
import {Http} from '@angular/http'
import {ProductTypeJsonSerializerService} from 'app/services/network/serializers/product-type-json.service'
import {ProductTypeJson} from 'app/services/network/serializers/product-type-json.service'


@Injectable()
export class ProductTypeNetworkService {
    constructor(
        private http: Http,
        private jsonSerializer: ProductTypeJsonSerializerService,
    ) { }

    async get(pk: PrimaryKey): Promise<ProductType> {
        let response = await this.http.request(`/api/shuup/product_type/${pk}/`)
            .first()
            .toPromise()
        let productTypeJson: ProductTypeJson = response.json()
        return this.jsonSerializer.deserialize(productTypeJson)
    }

    async getAll(): Promise<Array<ProductType>> {
        let response = await this.http.request('/api/shuup/product_type/')
            .first()
            .toPromise()
        let productTypeArrayJson: Array<ProductTypeJson> = response.json()
        return this.jsonSerializer.deserializeArray(productTypeArrayJson)
    }
}
