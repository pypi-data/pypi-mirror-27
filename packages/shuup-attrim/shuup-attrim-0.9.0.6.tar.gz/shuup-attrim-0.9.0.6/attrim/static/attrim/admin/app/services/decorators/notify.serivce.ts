export function asyncNotifyOn(messages: {success: Optional<string>, error: string}) {
    return (target: Object, propertyKey: string, descriptor: TypedPropertyDescriptor<any>) => {
        let originalMethod = descriptor.value
        descriptor.value = async function(...args: any[]): Promise<any> {
            let result: any
            try {
                result = await originalMethod.apply(this, args);
                if (messages.success !== null) {
                    (this as any).notifyService.success(messages.success);
                }
            } catch (error) {
                (this as any).notifyService.error(messages.error, error);
            }
            return result
        }
        return descriptor
    }
}
