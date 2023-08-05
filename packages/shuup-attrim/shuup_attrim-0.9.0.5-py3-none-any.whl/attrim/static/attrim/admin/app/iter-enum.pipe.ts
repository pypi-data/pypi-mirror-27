import {Pipe} from '@angular/core'
import {PipeTransform} from '@angular/core'


@Pipe({name: 'iterEnum'})
export class IterateEnumPipe implements PipeTransform {
    transform(enumObj: any, args: Array<string>): EnumForIteration {
        let enumForIteration: EnumForIteration = []
        let enumIndexes: Array<EnumValue> = Object.keys(enumObj).filter(Number) as any
        for (let enumIndex of enumIndexes) {
            enumForIteration.push({value: enumIndex, name: enumObj[enumIndex]})
        }
        return enumForIteration
    }
}


type EnumForIteration = Array<{value: EnumValue, name: EnumName}>

type EnumValue = number

type EnumName = string
