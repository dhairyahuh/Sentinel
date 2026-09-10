import { Link } from 'react-router-dom'
import { useDefend, useSummary } from '@/api/queries'
import { count, pct } from '@/lib/format'
import { verdict as separabilityVerdict } from '@/lib/fidelity'

/**
 * The whole submission in one line per stage.
 *
 * A judge at a conference sees a lot of consoles and has a few minutes for each.
 * The live stream below this strip is the product; this strip is the *argument*,
 * and without it a reader has to visit four routes and assemble it themselves.
 *
 * Sentinel's four stages — map, simulate, detect, evolve — are a cycle, not
 * a sequence. Each cell shows a measured quantity from this run.
 *
 * YEL Track 2 — Tracing Financial Crime Across Patterns.
 */
export function Argument() {
  const summary = useSummary()
  const defend = useDefend()

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const s = (summary.data?.summary ?? {}) as Record<string, any>
  const identify = s.identify ?? {}
  const generate = s.generate ?? {}
  const rounds = Array.isArray(s.loop) ? s.loop : []
  const convergence = s.loop_convergence ?? null

  const families = identify.families ? Object.keys(identify.families).length : null

  // The single most persuasive comparison in the run: what ten hand-written
  // conditions catch, against what the ensemble catches on the same rows.
  const baselines = defend.data?.baselines.rows ?? []
  const ensemble = baselines.find((r) => String(r.model).startsWith('ensemble'))
  const rules = baselines.find((r) => String(r.model) === 'expert_rules')

  const derived = generate.derived_separability_recall ?? null
  const saturated = separabilityVerdict(derived) === 'saturated'

  if (summary.isLoading) return <div className="h-[64px] shrink-0" aria-busy="true" />

  return (
    <div className="flex shrink-0 items-stretch gap-px overflow-x-auto rounded border border-line-subtle bg-surface">
      <Cell
        to="/identify"
        pillar="map"
        tone="text-accent"
        figure={count(identify.total_vectors)}
        unit="crime patterns"
        claim={
          <>
            across {count(families)} criminal families,{' '}
            <span className="num">{count(identify.simulated_vectors)}</span> simulated
            and measured across accounts and time
          </>
        }
      />

      <Cell
        to="/generate"
        pillar="simulate"
        tone="text-accent"
        figure={count(generate.transactions)}
        unit="transactions across scenario"
        claim={
          saturated ? (
            <span className="text-amber">
              separability past the pipeline&apos;s own ceiling — detection figures are an upper bound
            </span>
          ) : (
            <>
              at a <span className="num">{pct(generate.fraud_rate, 2)}</span> crime rate,
              validated on {count(11)} fidelity checks
            </>
          )
        }
      />

      <Cell
        to="/defend"
        pillar="detect"
        tone="text-accent"
        figure={pct(ensemble?.recall as number | null)}
        unit="of crime patterns caught"
        claim={
          rules ? (
            <>
              against <span className="num">{pct(rules.recall as number | null)}</span> for ten
              hand-written rules, same transactions, same budget
            </>
          ) : (
            'at the deployed false-positive budget'
          )
        }
      />

      <Cell
        to="/loop"
        pillar="evolve"
        tone="text-red"
        figure={count(rounds.length)}
        unit="adaptive evolution rounds"
        claim={
          convergence ? (
            <span className={String(convergence.verdict).startsWith('diverging') ? 'text-amber' : ''}>
              {String(convergence.verdict).split(':')[0]} — reported as the pipeline computed it
            </span>
          ) : (
            'crime patterns mutate, detector adapts, survivors rejoin the map'
          )
        }
      />
    </div>
  )
}

function Cell({
  to,
  pillar,
  tone,
  figure,
  unit,
  claim,
}: {
  to: string
  pillar: string
  tone: string
  figure: string
  unit: string
  claim: React.ReactNode
}) {
  return (
    <Link
      to={to}
      className="min-w-52 flex-1 border-r border-line-subtle px-3 py-2 transition-colors last:border-r-0 hover:bg-hover"
    >
      <div className={`label ${tone}`}>{pillar}</div>
      <div className="flex items-baseline gap-1.5">
        <span className="num text-lg leading-none text-fg">{figure}</span>
        <span className="truncate text-2xs text-fg-muted">{unit}</span>
      </div>
      <div className="mt-0.5 line-clamp-2 text-2xs leading-snug text-fg-faint">{claim}</div>
    </Link>
  )
}
