import { useEffect, useState, useCallback } from 'react'
import { useTour } from '@/features/tour/useTour'
import { Panel } from '@/components/ui/Panel'
import { PanelLoading, NoArtefact } from '@/components/ui/RouteSkeleton'
import { ErrorBoundary } from '@/components/ui/ErrorBoundary'
import { StreamTable } from '@/features/console/StreamTable'
import { CounterRail } from '@/features/console/Counters'
import { Headline } from '@/features/console/Headline'
import { Argument } from '@/features/console/Argument'
import { useStream } from '@/features/console/useStream'
import { Inspector } from '@/features/inspector/Inspector'
import { useDefend, useTransactions } from '@/api/queries'
import { fprBudget, metric } from '@/lib/tables'
import { count } from '@/lib/format'

/**
 * `/` — the Live Transaction Feed.
 *
 * The first thing a judge sees is what Sentinel would look like if it shipped:
 * transactions arriving, being scored against crime patterns, and being stopped
 * or let through, with the full explanation one click away.
 *
 * Sentinel answers YEL Track 2 Problem 5: tracing financial crime that only
 * becomes visible across many transactions or accounts over time. The stream
 * here is the real-time face of that — the detector underneath it is trained
 * on cross-account, cross-time patterns, not individual transaction signals.
 *
 * The single most important honesty claim on this screen is in the panel
 * caveat, so it is worth stating here too: **the rows are real and the arrival
 * is not.** Every payment shown was scored by the trained ensemble during the
 * run and its score, decision and label come straight out of
 * `defend_scored_test_set.csv`. What the browser does is decide *when* to show
 * you each one. Nothing is generated client-side.
 */
export default function Console() {
  const [selected, setSelected] = useState<string | null>(null)

  // A large first page rather than paging as the stream advances: the cursor
  // walks a fixed slice, and re-fetching mid-demo would stutter the stream at
  // exactly the moment someone is watching it.
  const txns = useTransactions({ limit: 2000 })
  const defend = useDefend()

  const stream = useStream(txns.data?.rows)

  // The tour opens the inspector on an alerted payment rather than whatever
  // happens to be at the top of the stream. An approved row would be a
  // perfectly honest thing to show and a wasted step - the reason codes, the
  // counterfactual and the guard verdict are the point, and an approval has
  // none of them.
  const rows = txns.data?.rows
  useEffect(() => {
    return useTour.getState().register('open-inspector', () => {
      const interesting =
        rows?.find((r) => r.intent_block === 1 || r.control_block === 1) ??
        rows?.find((r) => r.is_fraud === 1 && r.decision === 1) ??
        rows?.find((r) => r.decision === 1)
      if (interesting) setSelected(interesting.txn_id)
    })
  }, [rows])

  const headline = defend.data?.headline
  const budget = fprBudget(defend.data?.intervals)
  const recall = metric(headline, 'recall')

  return (
    <div className="flex h-full min-h-0 flex-col gap-2 p-2">
      {/* YEL hero banner — communicates the problem statement within 30 seconds.
          A judge who reads only this strip has the track, the problem, and the
          claim. Dismiss-able so it doesn't eat space during a live demo. */}
      <HeroBanner />

      {/* The argument strip: four measured quantities, one per stage. */}
      <ErrorBoundary label="Run summary">
        <Argument />
      </ErrorBoundary>

      <ErrorBoundary label="Headline metrics">
        <Headline />
      </ErrorBoundary>

      <div className="flex min-h-0 flex-1 gap-2">
        <Panel
          id="tour-stream"
          title="Live payment stream"
          source="defend_scored_test_set.csv"
          subtitle={
            <>
              Transactions the trained model scored during this run, replayed in arrival order.{' '}
              {txns.data ? (
                <>
                  <span className="num text-fg-secondary">{count(stream.total)}</span> rows
                  loaded of{' '}
                  <span className="num text-fg-secondary">{count(txns.data.total)}</span> in
                  the scenario window.
                </>
              ) : null}
            </>
          }
          actions={
            <StreamControls
              running={stream.running}
              rate={stream.rate}
              onToggle={stream.toggle}
              onRate={stream.setRate}
              onReset={stream.reset}
            />
          }
          caveat={
            <>
              <span className="text-fg-muted">The rows are real; the arrival is not.</span>{' '}
              Every transaction here was scored by the ensemble during the run — score, decision
              and outcome come from the artefact, unmodified. The browser only decides when to
              show each one. Two decline types are kept distinct on purpose: a{' '}
              <span className="text-red">provable block</span> can be shown to a customer and
              argued with, an <span className="text-amber">alert</span> is a probability.
            </>
          }
          className="min-w-0 flex-1"
          scroll
        >
          {txns.isLoading ? (
            <PanelLoading />
          ) : !txns.data?.available ? (
            <NoArtefact
              file="defend_scored_test_set.csv"
              note="The defend stage writes this. A run that stopped before it has nothing to stream."
            />
          ) : (
            <StreamTable rows={stream.rows} onSelect={setSelected} selected={selected} />
          )}
        </Panel>

        <Panel
          id="tour-counters"
          title="Since you started watching"
          source="defend_scored_test_set.csv"
          className="w-[260px] shrink-0"
        >
          <CounterRail
            counters={stream.counters}
            fprBudget={budget}
            measuredRecall={recall}
          />
        </Panel>
      </div>

      <Inspector txnId={selected} onClose={() => setSelected(null)} />
    </div>
  )
}

function StreamControls({
  running,
  rate,
  onToggle,
  onRate,
  onReset,
}: {
  running: boolean
  rate: number
  onToggle: () => void
  onRate: (n: number) => void
  onReset: () => void
}) {
  return (
    <div className="flex items-center gap-1">
      {/* Pause exists because the stream is the demo's biggest liability: a row
          worth talking about scrolls away in four seconds. Being able to freeze
          it is the difference between narrating the console and chasing it. */}
      <button
        type="button"
        onClick={onToggle}
        className="rounded border border-line px-2 py-0.5 font-display text-2xs font-semibold uppercase tracking-wider text-fg-secondary transition-colors hover:bg-hover hover:text-fg"
      >
        {running ? 'Pause' : 'Resume'}
      </button>
      <label className="flex items-center gap-1" title="Rows per second">
        <select
          value={rate}
          onChange={(e) => onRate(Number(e.target.value))}
          className="rounded border border-line bg-surface px-1 py-0.5 font-mono text-2xs text-fg-secondary"
        >
          {[2, 4, 8, 16, 32].map((r) => (
            <option key={r} value={r}>
              {r}/s
            </option>
          ))}
        </select>
      </label>
      <button
        type="button"
        onClick={onReset}
        title="Clear the buffer and the counters, and start the cursor again"
        className="rounded border border-line px-2 py-0.5 font-display text-2xs font-semibold uppercase tracking-wider text-fg-muted transition-colors hover:bg-hover hover:text-fg"
      >
        Reset
      </button>
    </div>
  )
}

/**
 * YEL hero banner.
 *
 * A dismissible strip that communicates the Track 2 problem statement, the
 * target user, and Sentinel's solution within approximately 30 seconds of
 * landing on the page. Dismissed state is stored in sessionStorage so it
 * persists within a demo session but resets between them.
 */
function HeroBanner() {
  const [dismissed, setDismissed] = useState(() => {
    try { return sessionStorage.getItem('sentinel.hero.dismissed') === '1' } catch { return false }
  })

  const dismiss = useCallback(() => {
    setDismissed(true)
    try { sessionStorage.setItem('sentinel.hero.dismissed', '1') } catch { /* private browsing */ }
  }, [])

  if (dismissed) return null

  return (
    <div className="shrink-0 rounded border border-accent-dim bg-accent-wash px-4 py-3">
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0 flex-1">
          <div className="mb-1 flex flex-wrap items-center gap-2">
            <span className="rounded border border-accent-dim bg-surface px-1.5 py-0.5 font-display text-2xs font-semibold uppercase tracking-wider text-accent">
              YEL Track 2 · Problem 5
            </span>
            <span className="font-display text-xs font-semibold text-fg">
              Tracing Financial Crime Across Patterns
            </span>
          </div>
          <p className="text-2xs leading-relaxed text-fg-secondary">
            <span className="text-fg font-medium">The problem:</span>{' '}
            Financial crime — mule rings, APP fraud campaigns, ATO waves — is invisible
            in any single transaction. It only becomes detectable across accounts and time.{' '}
            <span className="text-fg font-medium">Sentinel’s answer:</span>{' '}
            map 67 crime patterns across 9 criminal families, simulate realistic cross-account
            scenarios, train a pattern detector, then run an adaptive loop that discovers how
            criminals evolve and feeds those mutations back into the map.
          </p>
        </div>
        <div className="flex shrink-0 items-center gap-2">
          <button
            type="button"
            onClick={() => useTour.getState().start()}
            className="rounded border border-accent-dim bg-accent px-2.5 py-1 font-display text-2xs font-semibold uppercase tracking-wider text-accent-fg transition-colors hover:opacity-90"
          >
            ▸ Start demo
          </button>
          <button
            type="button"
            onClick={dismiss}
            title="Dismiss this banner"
            aria-label="Dismiss"
            className="rounded border border-line px-2 py-1 font-display text-2xs font-semibold uppercase tracking-wider text-fg-muted transition-colors hover:bg-hover hover:text-fg"
          >
            ×
          </button>
        </div>
      </div>
    </div>
  )
}
