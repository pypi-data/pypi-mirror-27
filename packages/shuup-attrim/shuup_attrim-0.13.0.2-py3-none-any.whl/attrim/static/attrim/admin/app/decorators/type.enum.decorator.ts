import {Type} from 'app/type.enum'


/**
 * Allows to use the `Type` enum directly in templates.
 */
export function TypeEnumDecorator(constructor: Function) {
    constructor.prototype.Type = Type
}
