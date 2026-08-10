export default function DataTable({ columns, rows, emptyText = "No records available.", caption = null }) {
  return (
    <div className="app-panel overflow-hidden">
      {caption ? (
        <div className="border-b border-slate-200 px-4 py-3 text-[13px] font-medium text-slate-700">{caption}</div>
      ) : null}
      <div className="overflow-x-auto">
        <table className="min-w-full table-auto text-left text-[13px]">
          <thead className="bg-slate-100 text-slate-700">
            <tr>
              {columns.map((column) => (
                <th key={column.key} className="border-b border-slate-200 px-4 py-3 font-semibold">
                  {column.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white text-slate-800">
            {rows.length ? (
              rows.map((row, index) => (
                <tr key={row.id || index} className="align-top even:bg-slate-50/60 hover:bg-sky-50/50">
                  {columns.map((column) => (
                    <td key={column.key} className="border-b border-slate-200 px-4 py-3 leading-5">
                      {column.render ? column.render(row[column.key], row) : row[column.key] || "--"}
                    </td>
                  ))}
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={columns.length} className="px-4 py-8 text-center text-slate-500">
                  {emptyText}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
