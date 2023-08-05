"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const type_enum_1 = require("app/type.enum");
/**
 * Allows to use the `Type` enum directly in templates.
 */
function TypeEnumDecorator(constructor) {
    constructor.prototype.Type = type_enum_1.Type;
}
exports.TypeEnumDecorator = TypeEnumDecorator;
//# sourceMappingURL=type.enum.decorator.js.map