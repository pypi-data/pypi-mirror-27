import {TransStr} from 'app/models/trans-str.model'
import {Type} from 'app/type.enum'


export class Option {
    pk: Optional<PrimaryKey> = null
    clsPk: Optional<PrimaryKey> = null
    type: Type
    order: Optional<number> = null
    /**
     * Must have a default object `{}`, otherwise it'll screw up
     * the sharing of the `value` between OptionComponent and its child
     * TransStrComponent.
     */
    value: OptionValue = {}
    isMarkedAsRemoved: boolean = false
    isSaved: boolean = false

    constructor(args: {
        pk?: Optional<PrimaryKey>
        clsPk?: Optional<PrimaryKey>
        type: Type
        order?: Optional<number>
        value?: OptionValue
        isMarkedAsRemoved?: boolean
        isSaved?: boolean
    }) {
        this.pk = args.pk ? args.pk : this.pk
        this.clsPk = args.clsPk ? args.clsPk : this.clsPk
        this.type = args.type
        this.order = args.order ? args.order : this.order
        this.value = args.value ? args.value : this.value
        if (args.isMarkedAsRemoved) {
            this.isMarkedAsRemoved = args.isMarkedAsRemoved
        }
        this.isSaved = args.isSaved ? args.isSaved : this.isSaved
    }
}


export type OptionValue = string | number | TransStr
