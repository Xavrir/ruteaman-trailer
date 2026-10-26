import React, { useEffect, useId, useMemo, useState } from 'react';
import { StyleSheet, View, type StyleProp, type ViewStyle } from 'react-native';
import Svg, { Circle, Defs, Ellipse, G, Path, RadialGradient, Stop } from 'react-native-svg';
import Animated, {
  Easing,
  cancelAnimation,
  useAnimatedStyle,
  useSharedValue,
  withDelay,
  withRepeat,
  withSequence,
  withSpring,
  withTiming,
} from 'react-native-reanimated';
import { useMotion, useUI } from '../theme';
import { springs } from '../tokens/motion';
import { mascotColors, type MascotColors } from '../tokens/colors';
import {
  BLINK_EVERY_MS,
  BREATHE_MS,
  FLUTTER_EVERY_MS,
  HOVER_MS,
  KUNANG_POSES,
  VIEWBOX,
  hoverLift,
  kunangMotionPlan,
  motionOrigins,
  paintFor,
  type KunangPose,
  type Shape,
} from './kunang-poses';

export interface KunangProps {
  pose: KunangPose;
  size?: number;
  /** Plays the Sampai settle on mount; pass false when the sheet is shown again for the same trip. */
  enter?: boolean;
  /** Only when the mascot carries meaning; otherwise it stays hidden from screen readers. */
  accessibilityLabel?: string;
  style?: StyleProp<ViewStyle>;
}

const SETTLE_DROP = 6;
const breathe = Easing.inOut(Easing.sin);

function ShapeView({ shape, colors }: { shape: Shape; colors: MascotColors }) {
  const p = paintFor(shape, colors);
  const paint = {
    fill: p.fill,
    fillOpacity: p.fillOpacity,
    stroke: p.stroke,
    strokeWidth: p.strokeWidth,
    strokeLinecap: 'round' as const,
    strokeLinejoin: 'round' as const,
  };
  if (shape.kind === 'path') return <Path d={shape.d} {...paint} />;
  if (shape.kind === 'circle') return <Circle cx={shape.cx} cy={shape.cy} r={shape.r} {...paint} />;
  return <Ellipse cx={shape.cx} cy={shape.cy} rx={shape.rx} ry={shape.ry} {...paint} />;
}

function Layer({ size, rotate, children }: { size: number; rotate: number; children: React.ReactNode }) {
  return (
    <Svg width={size} height={size} viewBox={`0 0 ${VIEWBOX} ${VIEWBOX}`}>
      <G rotation={rotate} origin={`${VIEWBOX / 2}, ${VIEWBOX / 2}`}>
        {children}
      </G>
    </Svg>
  );
}

/** Kunang, the RuteAman firefly. Decorative by default; never place it in SOS, Guardian or navigation. */
export function Kunang({ pose, size = 96, enter = true, accessibilityLabel, style }: KunangProps) {
  const { scheme } = useUI();
  const motion = useMotion();
  const colors = mascotColors[scheme];
  const g = KUNANG_POSES[pose].geometry;
  const origins = useMemo(() => motionOrigins(pose), [pose]);
  const plan = kunangMotionPlan(pose, motion.reduced, enter);
  // SVG ids are document-wide on some renderers; React's ids contain colons that break url(#…).
  const id = `kunang${useId().replace(/[^a-zA-Z0-9]/g, '')}`;
  // Instances on one screen should not blink in step.
  const [blinkOffset] = useState(() => Math.round(Math.random() * 1600));

  const glow = useSharedValue(1);
  const hover = useSharedValue(0);
  const lift = hoverLift(size);
  const lid = useSharedValue(1);
  const flap = useSharedValue(1);
  const drop = useSharedValue(plan.settle ? -SETTLE_DROP : 0);
  const grow = useSharedValue(plan.settle ? 0.94 : 1);

  useEffect(() => {
    if (plan.breathe) {
      glow.set(withRepeat(withTiming(0.55, { duration: BREATHE_MS / 2, easing: breathe }), -1, true));
      hover.set(withRepeat(withTiming(1, { duration: HOVER_MS / 2, easing: breathe }), -1, true));
    } else {
      cancelAnimation(glow);
      cancelAnimation(hover);
      glow.set(1);
      hover.set(0);
    }
    if (plan.blink) {
      lid.set(
        withDelay(
          blinkOffset,
          withRepeat(withSequence(withDelay(BLINK_EVERY_MS, withTiming(0.1, { duration: 70 })), withTiming(1, { duration: 120 })), -1)
        )
      );
    } else {
      cancelAnimation(lid);
      lid.set(1);
    }
    if (plan.flutter) {
      flap.set(
        withRepeat(
          withSequence(
            withDelay(FLUTTER_EVERY_MS, withTiming(0.86, { duration: 110 })),
            withTiming(1, { duration: 110 }),
            withTiming(0.88, { duration: 110 }),
            withTiming(1, { duration: 140 })
          ),
          -1
        )
      );
    } else {
      cancelAnimation(flap);
      flap.set(1);
    }
    if (plan.settle) {
      drop.set(withSpring(0, springs.settle));
      grow.set(withSpring(1, springs.settle));
    } else {
      cancelAnimation(drop);
      cancelAnimation(grow);
      drop.set(0);
      grow.set(1);
    }
    return () => {
      cancelAnimation(glow);
      cancelAnimation(hover);
      cancelAnimation(lid);
      cancelAnimation(flap);
    };
  }, [plan.breathe, plan.blink, plan.flutter, plan.settle, blinkOffset, glow, hover, lid, flap, drop, grow]);

  const rootStyle = useAnimatedStyle(() => ({
    transform: [{ translateY: drop.get() - hover.get() * lift }, { scale: grow.get() }],
  }));
  const glowStyle = useAnimatedStyle(() => ({
    opacity: glow.get(),
    transform: [{ scale: 0.92 + glow.get() * 0.1 }],
  }));
  const wingStyle = useAnimatedStyle(() => ({ transform: [{ scaleX: flap.get() }] }));
  const eyeStyle = useAnimatedStyle(() => ({ transform: [{ scaleY: lid.get() }] }));

  const box = { width: size, height: size };
  const a11y = accessibilityLabel
    ? { accessible: true, accessibilityRole: 'image' as const, accessibilityLabel }
    : { accessibilityElementsHidden: true, importantForAccessibility: 'no-hide-descendants' as const };

  return (
    <Animated.View pointerEvents="none" style={[box, rootStyle, style]} {...a11y}>
      <Animated.View style={[StyleSheet.absoluteFill, { transformOrigin: [...origins.glow, 0] }, glowStyle]}>
        <Layer size={size} rotate={g.rotate}>
          <Defs>
            <RadialGradient id={`${id}h`}>
              <Stop offset="0" stopColor={colors.halo} stopOpacity={colors.haloOpacity} />
              <Stop offset="1" stopColor={colors.halo} stopOpacity={0} />
            </RadialGradient>
          </Defs>
          <Circle cx={g.halo.cx} cy={g.halo.cy} r={g.halo.r} fill={`url(#${id}h)`} />
        </Layer>
      </Animated.View>
      <Animated.View style={[StyleSheet.absoluteFill, { transformOrigin: [...origins.wings, 0] }, wingStyle]}>
        <Layer size={size} rotate={g.rotate}>
          {g.wings.map((s, i) => (
            <ShapeView key={i} shape={s} colors={colors} />
          ))}
        </Layer>
      </Animated.View>
      <View style={StyleSheet.absoluteFill}>
        <Svg width={size} height={size} viewBox={`0 0 ${VIEWBOX} ${VIEWBOX}`}>
          <Defs>
            <RadialGradient id={`${id}c`}>
              <Stop offset="0" stopColor={colors.core} stopOpacity={1} />
              <Stop offset="0.55" stopColor={colors.core} stopOpacity={0.9} />
              <Stop offset="1" stopColor={colors.coreEdge} stopOpacity={colors.coreEdgeOpacity} />
            </RadialGradient>
          </Defs>
          <G rotation={g.rotate} origin={`${VIEWBOX / 2}, ${VIEWBOX / 2}`}>
            <Ellipse cx={g.core.cx} cy={g.core.cy} rx={g.core.rx} ry={g.core.ry} fill={`url(#${id}c)`} />
            {g.body.map((s, i) => (
              <ShapeView key={i} shape={s} colors={colors} />
            ))}
          </G>
          {g.extras.map((s, i) => (
            <ShapeView key={i} shape={s} colors={colors} />
          ))}
        </Svg>
      </View>
      <Animated.View style={[StyleSheet.absoluteFill, { transformOrigin: [...origins.eyes, 0] }, eyeStyle]}>
        <Layer size={size} rotate={g.rotate}>
          {g.eyes.map((s, i) => (
            <ShapeView key={i} shape={s} colors={colors} />
          ))}
        </Layer>
      </Animated.View>
    </Animated.View>
  );
}
