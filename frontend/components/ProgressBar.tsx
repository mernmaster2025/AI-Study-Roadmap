export default function ProgressBar({ value }: { value: number }) {
  const pct = Math.max(0, Math.min(100, value));
  return (
    <div className="h-2.5 w-full overflow-hidden rounded-full bg-gray-200 dark:bg-gray-800">
      <div
        className="h-full rounded-full bg-brand-600 transition-all duration-500"
        style={{ width: `${pct}%` }}
      />
    </div>
  );
}
