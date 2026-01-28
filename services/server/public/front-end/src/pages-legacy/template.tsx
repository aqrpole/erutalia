export default function Index () {
    return (
        <h1>Hello Next.js
            <div className="border p-4">
                Border should be visible
            </div>
            <button className="bg-primary text-primary-foreground px-4 py-2">
                Test
            </button>
            <input className="border border-input focus:ring-2 focus:ring-ring px-2" />
            <div className="bg-destructive text-destructive-foreground p-2">Delete</div>
        </h1>
    );
}
