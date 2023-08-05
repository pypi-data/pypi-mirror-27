"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
class Cls {
    constructor(args) {
        this.pk = null;
        this.name = {};
        this.optionsPk = [];
        this.isSaved = false;
        this.pk = args.pk ? args.pk : this.pk;
        this.code = args.code;
        this.type = args.type;
        this.name = args.name ? args.name : this.name;
        this.productType = args.productType;
        this.optionsPk = args.optionsPk ? args.optionsPk : this.optionsPk;
        this.isSaved = args.isSaved ? args.isSaved : this.isSaved;
    }
}
exports.Cls = Cls;
//# sourceMappingURL=cls.model.js.map