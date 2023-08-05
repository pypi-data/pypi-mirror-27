import {Type} from 'app/type.enum'
import {TransStr} from 'app/models/trans-str.model'
import {ProductType} from 'app/models/product-type.model'


export class Cls {
    pk: Optional<number> = null
    code: string
    type: Type
    name: TransStr = {}
    productType: ProductType
    optionsPk: Array<PrimaryKey> = []
    isSaved: boolean = false

    constructor(args: {
        pk?: Optional<number>
        code: string
        type: Type
        name?: TransStr
        productType: ProductType
        optionsPk?: Optional<Array<PrimaryKey>>
        isSaved?: boolean
    }) {
        this.pk = args.pk ? args.pk : this.pk
        this.code = args.code
        this.type = args.type
        this.name = args.name ? args.name : this.name
        this.productType = args.productType
        this.optionsPk = args.optionsPk ? args.optionsPk : this.optionsPk
        this.isSaved = args.isSaved ? args.isSaved : this.isSaved
    }
}
