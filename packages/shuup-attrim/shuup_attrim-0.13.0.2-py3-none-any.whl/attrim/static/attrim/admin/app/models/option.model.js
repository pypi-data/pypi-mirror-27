"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
class Option {
    constructor(args) {
        this.pk = null;
        this.clsPk = null;
        this.order = null;
        /**
         * Must have a default object `{}`, otherwise it'll screw up
         * the sharing of the `value` between OptionComponent and its child
         * TransStrComponent.
         */
        this.value = {};
        this.isMarkedAsRemoved = false;
        this.isSaved = false;
        this.pk = args.pk ? args.pk : this.pk;
        this.clsPk = args.clsPk ? args.clsPk : this.clsPk;
        this.type = args.type;
        this.order = args.order ? args.order : this.order;
        this.value = args.value ? args.value : this.value;
        if (args.isMarkedAsRemoved) {
            this.isMarkedAsRemoved = args.isMarkedAsRemoved;
        }
        this.isSaved = args.isSaved ? args.isSaved : this.isSaved;
    }
}
exports.Option = Option;
//# sourceMappingURL=option.model.js.map